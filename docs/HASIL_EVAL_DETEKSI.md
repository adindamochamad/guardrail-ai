# Hasil evaluasi deteksi AI (set kecil, MVP)

Jalankan ulang:

```bash
backend/.venv/bin/python scripts/eval_deteksi.py
```

Data berlabel: [`backend/tests/fixtures_eval_deteksi.json`](../backend/tests/fixtures_eval_deteksi.json) (8 sampel, heuristik **tanpa LLM**).

## Snapshot terakhir (VPS)

| Metrik | Nilai |
|--------|--------|
| Sampel | 8 |
| Akurasi | 0,625 |
| Precision | 1,0 |
| Recall | 0,25 |
| F1 | 0,4 |
| Ambang | 0,55 |

**Confusion:** TP=1, FP=0, TN=4, FN=3

## Interpretasi untuk Devpost

- Gunakan sebagai **evaluasi awal / proof of method**, bukan klaim **85%+** produksi.
- Recall rendah: banyak pola “AI” di set belum terpicu tanpa trailer Copilot / LLM — perlu perluasan dataset atau turunkan ambang hanya setelah uji.
- Precision 1,0 pada set ini: tidak ada false positive.

## Langkah perbaikan (opsional)

1. Tambah sampel di `backend/tests/fixtures_eval_deteksi.json`.
2. Uji dengan `pesan_commit` Copilot pada lebih banyak kasus.
3. Bandingkan dengan `gunakan_llm: true` (butuh `OPENAI_API_KEY`) — terpisah dari metrik di atas.
