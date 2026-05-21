#!/usr/bin/env bash
#
# Hook Cursor (event stop): jalankan agensi QA lalu tulis ringkasan ke log proyek.
# Skrip TIDAK gagalkan sesi Cursor (exit 0) agar alur Anda tetap lancar; baca exit QA di dalam log.
#
set +euo pipefail

bin_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
akar_repo="$(cd "${bin_dir}/../.." && pwd)"
log_folder="${akar_repo}/.cursor"
mkdir -p "${log_folder}"
log_qa="${log_folder}/qa-setelah-agent-terakhir.log"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >>"${log_qa}"
echo "stop hook QA — $(date -Iseconds)" >>"${log_qa}"
bash "${akar_repo}/scripts/agensi_verifikasi_qa.sh" >>"${log_qa}" 2>&1
kode_silang=$?
echo "... agensi QA selesai — kode keluar: ${kode_silang}" >>"${log_qa}"
exit 0
