"""Tes heuristik metadata commit."""

from src.ai_detector.metadata_git import skor_dari_metadata_git


def test_copilot_trailer_tinggi():
    pesan = "feat: x\n\nCo-authored-by: GitHub Copilot <noreply@github.com>"
    skor, rincian = skor_dari_metadata_git(pesan)
    assert skor >= 0.9
    assert rincian["terdeteksi"] is True


def test_tanpa_pesan_nol():
    skor, rincian = skor_dari_metadata_git(None)
    assert skor == 0.0
    assert rincian["terdeteksi"] is False
