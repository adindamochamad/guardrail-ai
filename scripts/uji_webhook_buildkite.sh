#!/usr/bin/env bash
# Uji webhook Buildkite ke API produksi (membaca token dari backend/.env).
set -euo pipefail

akar_repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
berkas_env="${akar_repo}/backend/.env"
url_api="${GUARDRAIL_URL:-https://guardrail-api.adindamochamad.com}"
url_api="${url_api%/}"

if [ ! -f "$berkas_env" ]; then
  echo "uji_webhook: tidak menemukan ${berkas_env}" >&2
  exit 2
fi

# Hanya baca baris BUILDKITE_* (hindari `source` penuh — APP_NAME bisa berisi spasi).
token=$(grep -E '^BUILDKITE_WEBHOOK_TOKEN=' "$berkas_env" | cut -d= -f2- | tr -d '"' | tr -d "'")
slug_org=$(grep -E '^BUILDKITE_ORG_SLUG=' "$berkas_env" | cut -d= -f2- | tr -d '"' | tr -d "'")
if [ -z "$token" ]; then
  echo "uji_webhook: BUILDKITE_WEBHOOK_TOKEN kosong di .env" >&2
  exit 2
fi

muatan='{
  "event": "build.finished",
  "build": {
    "number": 99,
    "message": "test guardrail webhook\n\ndef demo():\n    subprocess.call(\"ls\", shell=True)\n",
    "state": "passed"
  },
  "pipeline": {"slug": "guardrail-ai", "repository": ""},
  "organization": {"slug": "'"${slug_org:-demo-org}"'"}
}'

echo "uji_webhook: POST ${url_api}/webhooks/buildkite ..." >&2
berkas_respon=$(mktemp)
trap 'rm -f "$berkas_respon"' EXIT
kode_http=$(curl -sS -w '%{http_code}' -o "$berkas_respon" \
  -X POST "${url_api}/webhooks/buildkite" \
  -H "Content-Type: application/json" \
  -H "X-Buildkite-Token: ${token}" \
  -d "$muatan")

echo "HTTP ${kode_http}" >&2
if command -v jq >/dev/null 2>&1; then
  jq '{keaslian_webhook, anotasi, anotasi_terkirim, deteksi: .deteksi.apakah_ai, ringkasan: .analisis.ringkasan_keparahan}' "$berkas_respon" 2>/dev/null || cat "$berkas_respon"
else
  cat "$berkas_respon"
fi

if [ "$kode_http" != "200" ]; then
  exit 1
fi
