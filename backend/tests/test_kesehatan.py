"""Tes endpoint kesehatan dan koneksi DB ringan."""


def test_health_mengembalikan_ok(klien_api):
    balasan = klien_api.get("/health")
    assert balasan.status_code == 200
    isi = balasan.json()
    assert isi["status"] == "ok"
    assert isi["service"] == "GuardRail AI"


def test_db_ping_awal_bernomor_nol(klien_api):
    balasan = klien_api.get("/db/ping")
    assert balasan.status_code == 200
    isi = balasan.json()
    assert isi["status"] == "ok"
    assert isi["scans_count"] == 0
    assert isi["code_files_count"] == 0
