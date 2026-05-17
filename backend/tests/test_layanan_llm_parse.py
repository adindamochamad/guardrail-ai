"""Tes parser skor teks dari keluaran model."""

import pytest
from src.ai_detector.layanan_llm import _parse_skor_float


@pytest.mark.parametrize(
    ("teks", "diharapkan"),
    [
        ("0.73", 0.73),
        ("1.0", 1.0),
        ("0", 0.0),
        ("0.999", 0.999),
    ],
)
def test_parse_angka_valid(teks: str, diharapkan: float):
    assert _parse_skor_float(teks) == pytest.approx(diharapkan)


def test_parse_tak_valid():
    assert _parse_skor_float("bukan angka") is None
