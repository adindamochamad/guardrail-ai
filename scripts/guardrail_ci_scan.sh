#!/usr/bin/env bash
# Menggabungkan berkas .py terlacak Git, memanggil POST /scan, lalu gagal bila melewati ambang keparahan.
set -euo pipefail

akar_repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Hindari gagal `dubious ownership` saat repo dimiliki user lain (umum di VPS).
perintah_git=(git -c "safe.directory=${akar_repo}")

url_guardrail="${GUARDRAIL_URL:-http://127.0.0.1:8000}"
url_guardrail="${url_guardrail%/}"
ambang_gagal="${GUARDRAIL_FAIL_SEVERITY:-CRITICAL}"

batas_karakter="${GUARDRAIL_MAX_CHARS:-450000}"

if ! command -v curl >/dev/null 2>&1; then
  echo "guardrail_ci_scan: butuh perintah curl." >&2
  exit 2
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "guardrail_ci_scan: butuh perintah jq untuk membaca JSON respons." >&2
  exit 2
fi

if ! "${perintah_git[@]}" -C "${akar_repo}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "guardrail_ci_scan: jalankan di dalam repositori Git." >&2
  exit 2
fi

# Mengumpulkan cuplikan kode agar muat ke badan JSON /scan (batas ~500k di API).
kumpulan_kode=""
while IFS= read -r jalan_berkas; do
  [ -z "$jalan_berkas" ] && continue
  if [ ! -f "$jalan_berkas" ]; then
    continue
  fi
  fragmen=$'\n\n# --- '"${jalan_berkas}"$' ---\n'
  fragmen+=$(cat "$jalan_berkas")
  if ((${#kumpulan_kode} + ${#fragmen} > batas_karakter)); then
    echo "guardrail_ci_scan: cuplikan dipotong di ${batas_karakter} karakter (atur GUARDRAIL_MAX_CHARS)." >&2
    break
  fi
  kumpulan_kode+="$fragmen"
done < <("${perintah_git[@]}" -C "${akar_repo}" ls-files '*.py' | grep -vE '(^|/)(venv|\.venv|node_modules)/' || true)

if [ -z "${kumpulan_kode//[[:space:]]/}" ]; then
  echo "guardrail_ci_scan: tidak ada berkas .py terlacak untuk dipindai." >&2
  exit 0
fi

payload=$(jq -n --arg kode "$kumpulan_kode" '{
  kode: $kode,
  bahasa: "python",
  gunakan_llm: false
}')

echo "guardrail_ci_scan: memanggil ${url_guardrail}/scan ..." >&2
berkas_respon=$(mktemp)
trap 'rm -f "$berkas_respon"' EXIT
balasan_http=$(curl -sS -w '%{http_code}' -o "$berkas_respon" \
  -X POST "${url_guardrail}/scan" \
  -H 'Content-Type: application/json' \
  -d "$payload")
isi_balasan=$(cat "$berkas_respon")

if [ "$balasan_http" != "200" ]; then
  echo "guardrail_ci_scan: HTTP ${balasan_http}" >&2
  echo "$isi_balasan" >&2
  exit 1
fi

jumlah_critical=$(echo "$isi_balasan" | jq '.analisis.ringkasan_keparahan.CRITICAL // 0')
jumlah_high=$(echo "$isi_balasan" | jq '.analisis.ringkasan_keparahan.HIGH // 0')

echo "guardrail_ci_scan: ringkasan keparahan:" >&2
echo "$isi_balasan" | jq -c '.analisis.ringkasan_keparahan' >&2

gagal=false
if [ "$jumlah_critical" -gt 0 ]; then
  gagal=true
fi
if [ "$ambang_gagal" = "HIGH" ] || [ "$ambang_gagal" = "high" ]; then
  if [ "$jumlah_high" -gt 0 ]; then
    gagal=true
  fi
fi

if [ "$gagal" = true ]; then
  echo "guardrail_ci_scan: gagal — ada temuan pada ambang ${ambang_gagal} (CRITICAL=${jumlah_critical}, HIGH=${jumlah_high})." >&2
  echo "$isi_balasan" | jq '.analisis.daftar_temuan[:15]' >&2
  exit 1
fi

echo "guardrail_ci_scan: lolos (CRITICAL=${jumlah_critical}, HIGH=${jumlah_high})." >&2
exit 0
