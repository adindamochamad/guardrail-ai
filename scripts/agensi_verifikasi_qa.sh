#!/usr/bin/env bash
#
# Agensi verifikasi GuardRail AI — tes statis gabungan untuk backend dan frontend.
# Jalankan dari root repo:  bash scripts/agensi_verifikasi_qa.sh
# atau:                       make qa
#
set -euo pipefail

direktori_skrip="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
akar_repo="$(cd "${direktori_skrip}/.." && pwd)"
cd "${akar_repo}"

gagalan_turunan=0

perintah_ruff=""
perintah_pytest=""
perintah_python=""

if [[ -x "${akar_repo}/backend/.venv/bin/ruff" ]]; then
  perintah_ruff="${akar_repo}/backend/.venv/bin/ruff"
elif command -v ruff >/dev/null 2>&1; then
  perintah_ruff="$(command -v ruff)"
else
  perintah_ruff=""
fi

if [[ -x "${akar_repo}/backend/.venv/bin/pytest" ]]; then
  perintah_pytest="${akar_repo}/backend/.venv/bin/pytest"
elif command -v pytest >/dev/null 2>&1; then
  perintah_pytest="$(command -v pytest)"
fi

if [[ -x "${akar_repo}/backend/.venv/bin/python" ]]; then
  perintah_python="${akar_repo}/backend/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  perintah_python="$(command -v python3)"
fi

echo ":: BACKEND GUARDRAIL"
pushd backend >/dev/null

if [[ -n "${perintah_ruff}" ]]; then
  echo ">>> ruff check src tests"
  if ! ${perintah_ruff} check src tests; then
    gagalan_turunan=1
  fi
elif [[ -n "${perintah_python}" ]]; then
  echo ">>> ruff (modul) check src tests"
  if ! ${perintah_python} -m ruff check src tests; then
    gagalan_turunan=1
  fi
else
  echo "PERINGATAN: ruff tidak ditemukan; lewati lint backend."
fi

if [[ -n "${perintah_pytest}" ]]; then
  echo ">>> pytest -q"
  if ! ${perintah_pytest} -q; then
    gagalan_turunan=1
  fi
elif [[ -n "${perintah_python}" ]]; then
  echo ">>> pytest via python -m pytest -q"
  if ! ${perintah_python} -m pytest -q; then
    gagalan_turunan=1
  fi
else
  echo "PERINGATAN: pytest tidak ditemukan; lewati tes backend."
fi

popd >/dev/null

echo
echo ":: FRONTEND REACT/VITE"

if [[ -f "${akar_repo}/frontend/package.json" ]]; then
  if [[ ! -d "${akar_repo}/frontend/node_modules" ]]; then
    echo "LEWATI build frontend — node_modules belum ada. Jalankan: cd frontend && npm install"
  else
    pushd frontend >/dev/null
    echo ">>> npm run build"
    if ! npm run build; then
      gagalan_turunan=1
    fi
    popd >/dev/null
  fi
else
  echo "Tidak ada frontend/package.json — lewat."
fi

echo
if [[ "${gagalan_turunan}" -eq 0 ]]; then
  echo ">>>> Agensi QA: SEMUA LANGKAH LOLOS <<<<"
else
  echo ">>>> Agensi QA: ADA KEGAGALAN (periksa keluaran di atas) <<<<"
fi

exit "${gagalan_turunan}"
