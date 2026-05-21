#!/usr/bin/env python3
"""
Evaluasi cepat deteksi AI pada set berlabel kecil (MVP hackathon).
Jalankan dari root repo: backend/.venv/bin/python scripts/eval_deteksi.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

akar_repo = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(akar_repo / "backend"))

from src.ai_detector.mesin_deteksi import deteksi_ai  # noqa: E402
from src.config import PengaturanAplikasi  # noqa: E402

berkas_data = akar_repo / "backend" / "tests" / "fixtures_eval_deteksi.json"


def main() -> int:
    if not berkas_data.is_file():
        print(f"Data tidak ditemukan: {berkas_data}", file=sys.stderr)
        return 1

    sampel = json.loads(berkas_data.read_text(encoding="utf-8"))
    pengaturan = PengaturanAplikasi()

    benar = 0
    tp = fp = tn = fn = 0

    for item in sampel:
        hasil = deteksi_ai(
            item["kode"],
            pesan_commit=item.get("pesan_commit"),
            gunakan_llm=False,
            pengaturan=pengaturan,
        )
        pred = hasil.apakah_ai
        aktual = bool(item["label_apakah_ai"])
        if pred == aktual:
            benar += 1
        if pred and aktual:
            tp += 1
        elif pred and not aktual:
            fp += 1
        elif not pred and aktual:
            fn += 1
        else:
            tn += 1

    n = len(sampel)
    akurasi = benar / n if n else 0.0
    presisi = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * presisi * recall / (presisi + recall)
        if (presisi + recall) > 0
        else 0.0
    )

    ringkasan = {
        "jumlah_sampel": n,
        "benar": benar,
        "akurasi": round(akurasi, 3),
        "precision": round(presisi, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "confusion": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "ambang_batas": pengaturan.ambang_deteksi_ai,
        "catatan": "Heuristik tanpa LLM; set kecil — bukan klaim produksi 85%+.",
    }

    print(json.dumps(ringkasan, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
