"""Integrasi OpenAI untuk estimasi skor AI (opsional, membutuhkan kunci API)."""

from __future__ import annotations

import re

from ..config import PengaturanAplikasi


def perkiraan_skor_llm_bawaan(kode: str, pengaturan: PengaturanAplikasi) -> float | None:
    """
    Memanggil model chat ringkas; mengembalikan None jika tidak ada kunci atau gagal jaringan.

    Cuplikan kode dibatasi panjang agar biaya/token terkendali.
    """

    if not pengaturan.kunci_openai:
        return None

    # Impor malas agar modul tetap ringan jika OpenAI tidak terpasang di lingkungan minim.
    from openai import OpenAI

    potongan_kode = kode[:12000]

    try:
        klien = OpenAI(api_key=pengaturan.kunci_openai)
        balasan = klien.chat.completions.create(
            model=pengaturan.model_openai,
            temperature=0.1,
            max_tokens=24,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a classifier. Reply with exactly one number: "
                        "a probability between 0.0 and 1.0 that the user's code was "
                        "mostly written by an AI coding assistant. No words, only the number."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Code sample:\n```\n{potongan_kode}\n```",
                },
            ],
        )
    except Exception:
        return None

    teks = (balasan.choices[0].message.content or "").strip()
    return _parse_skor_float(teks)


def _parse_skor_float(teks: str) -> float | None:
    """Mengurai angka dari keluaran model; menyerah jika tidak ada bilangan valid."""

    cocok = re.search(
        r"(?P<angka>0(?:\.\d+)?|1(?:\.0+)?)\s*$",
        teks.replace(",", "."),
    )
    if not cocok:
        cocok_longgar = re.search(r"(?P<angka>0?\.\d+|1(?:\.0+)?)", teks.replace(",", "."))
        if not cocok_longgar:
            return None
        nilai = float(cocok_longgar.group("angka"))
    else:
        nilai = float(cocok.group("angka"))

    if nilai < 0.0 or nilai > 1.0:
        return None
    return nilai
