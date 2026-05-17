"""Tes verifikasi token / tanda HMAC webhook Buildkite."""

from __future__ import annotations

import hashlib
import hmac

from src.integrasi_buildkite.verifikasi_webhook import periksa_keaslian_webhook


def test_token_header_cocok() -> None:
    tubuh = b'{"event":"ping"}'
    lolos, alasan = periksa_keaslian_webhook(tubuh, "rahasia", None, "rahasia")
    assert lolos is True
    assert alasan == "token_ok"


def test_token_header_tidak_cocok() -> None:
    tubuh = b"{}"
    lolos, alasan = periksa_keaslian_webhook(tubuh, "salah", None, "rahasia")
    assert lolos is False
    assert alasan == "token_publik_tidak_cocok"


def test_tanpa_token_atau_tanda() -> None:
    lolos, alasan = periksa_keaslian_webhook(b"{}", None, None, "rahasia")
    assert lolos is False
    assert alasan == "tanpa_token_atau_tanda"


def test_tanda_hmac_valid() -> None:
    rahasia = "kunci-rahasia-webhook"
    tubuh = b'{"event":"build.finished"}'
    stempel = "1700000000"
    teks_tubuh = tubuh.decode("utf-8")
    gula_pesan = f"{stempel}.{teks_tubuh}".encode()
    tanda = hmac.new(rahasia.encode("utf-8"), gula_pesan, hashlib.sha256).hexdigest()
    header_tanda = f"timestamp={stempel},signature={tanda}"
    lolos, alasan = periksa_keaslian_webhook(
        tubuh,
        None,
        header_tanda,
        rahasia,
        waktu_sekarang=float(stempel),
    )
    assert lolos is True
    assert alasan == "tanda_ok"


def test_tanda_hmac_di_luar_jendela_replay() -> None:
    rahasia = "kunci"
    tubuh = b"{}"
    stempel = "1700000000"
    teks_tubuh = tubuh.decode("utf-8")
    gula_pesan = f"{stempel}.{teks_tubuh}".encode()
    tanda = hmac.new(rahasia.encode("utf-8"), gula_pesan, hashlib.sha256).hexdigest()
    header_tanda = f"timestamp={stempel},signature={tanda}"
    lolos, _ = periksa_keaslian_webhook(
        tubuh,
        None,
        header_tanda,
        rahasia,
        waktu_sekarang=float(stempel) + 9999,
    )
    assert lolos is False
