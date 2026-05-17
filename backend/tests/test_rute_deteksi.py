"""Tes HTTP untuk `POST /detect`."""


def test_detect_mengembalikan_struktur(klien_api):
    balasan = klien_api.post(
        "/detect",
        json={
            "kode": "def process_data(item):\n    return item\n",
            "gunakan_llm": False,
        },
    )
    assert balasan.status_code == 200
    isi = balasan.json()
    assert "apakah_ai" in isi
    assert "skor_keyakinan" in isi
    assert "ambang_batas" in isi
    assert "sinyal" in isi
    assert isi["sinyal"]["metadata_git"]["skor"] >= 0.0


def test_detect_kode_kosong_422(klien_api):
    balasan = klien_api.post("/detect", json={"kode": "", "gunakan_llm": False})
    assert balasan.status_code == 422
