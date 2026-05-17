"""Orkestrasi: parse muatan webhook → pemindaian → anotasi opsional."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any

from ..ai_detector import deteksi_ai
from ..analisis_risiko import analisis_kode
from ..config import PengaturanAplikasi
from .klien_anotasi import kirim_anotasi_build


def ringkas_muatan_build(muatan: dict[str, Any]) -> dict[str, Any]:
    """Mengekstrak bidang yang dipakai GuardRail dari JSON webhook pipeline."""

    acara = str(muatan.get("event") or "")
    bangun = muatan.get("build") or {}
    pipa = muatan.get("pipeline") or {}
    org = muatan.get("organization") or {}

    slug_org = str(org.get("slug") or "")
    slug_pipa = str(pipa.get("slug") or "")
    repo = str(pipa.get("repository") or "")

    return {
        "acara": acara,
        "nomor_build": bangun.get("number"),
        "cabang": bangun.get("branch"),
        "komit": bangun.get("commit"),
        "pesan_komit": bangun.get("message") or "",
        "slug_organisasi": slug_org,
        "slug_pipa": slug_pipa,
        "url_repositori": repo,
        "status_build": bangun.get("state"),
    }


def _kumpulkan_kode_untuk_pemindaian(
    ringkas: dict[str, Any],
    *,
    apakah_klon_git: bool,
    kedalaman_klon: int,
) -> tuple[str, str]:
    """Mengembalikan (teks_gabungan, sumber_info) untuk di-scan."""

    pesan = str(ringkas.get("pesan_komit") or "")
    if not apakah_klon_git or not ringkas.get("url_repositori"):
        return pesan, "pesan_komit"

    url_repo = str(ringkas["url_repositori"])
    cabang = ringkas.get("cabang")
    cuplikan, berhasil = _klon_dan_baca_berkas_python(
        url_repo,
        str(cabang) if cabang else None,
        kedalaman_klon,
    )
    if berhasil and cuplikan.strip():
        return cuplikan, "klon_git_ringkas"
    if pesan.strip():
        return pesan, "pesan_komit_fallback"
    return "", "kosong"


def _klon_dan_baca_berkas_python(
    url_repo: str,
    cabang: str | None,
    kedalaman: int,
    batas_berkas: int = 40,
    batas_panjang: int = 24000,
) -> tuple[str, bool]:
    """Klon --depth N (opsional cabang) dan gabungkan hingga N berkas .py."""

    try:
        with tempfile.TemporaryDirectory(prefix="guardrail_bk_") as folder_tmp:
            dest = Path(folder_tmp) / "repo"
            argumen = ["git", "clone", "--depth", str(kedalaman)]
            if cabang:
                argumen.extend(["--branch", cabang])
            argumen.extend([url_repo, str(dest)])

            hasil = subprocess.run(
                argumen,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            if hasil.returncode != 0:
                return "", False

            fragmen: list[str] = []
            total_karakter = 0
            jumlah = 0
            for jalan in sorted(dest.rglob("*.py")):
                if jumlah >= batas_berkas:
                    break
                relatif = jalan.relative_to(dest)
                try:
                    isi = jalan.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                potongan = f"\n\n# --- {relatif} ---\n{isi}"
                if total_karakter + len(potongan) > batas_panjang:
                    sisa = batas_panjang - total_karakter
                    if sisa > 200:
                        potongan = potongan[:sisa] + "\n# …dipotong…"
                        fragmen.append(potongan)
                    break
                fragmen.append(potongan)
                total_karakter += len(potongan)
                jumlah += 1
            return ("\n".join(fragmen), True)
    except (TimeoutError, subprocess.TimeoutExpired, OSError):
        return "", False


def taksir_gaya_anotasi(daftar_temuan: list[Any]) -> str:
    """Memetakan tingkat risiko tertinggi ke gaya anotasi Buildkite."""

    tertinggi = None
    for t in daftar_temuan:
        tingkat = getattr(t, "tingkat_keparahan", "")
        if tingkat == "CRITICAL":
            return "error"
        if tingkat == "HIGH" and tertinggi != "error":
            tertinggi = "warning"
        elif tingkat == "MEDIUM" and tertinggi is None:
            tertinggi = "warning"
    return tertinggi or "info"


def jalankan_pemindaian_dari_webhook(
    muatan: dict[str, Any],
    pengaturan: PengaturanAplikasi,
    *,
    apakah_klon_git: bool = False,
    kedalaman_klon: int = 1,
    klien_http: Any | None = None,
) -> dict[str, Any]:
    """
    Menjalankan deteksi AI + analisis risiko dan mengirim anotasi bila token API ada.

    Tidak melempar pengecualian ke atas — kesalahan dicatat dalam kamus respons.
    """

    ringkas = ringkas_muatan_build(muatan)
    teks_kode, sumber_teks = _kumpulkan_kode_untuk_pemindaian(
        ringkas,
        apakah_klon_git=apakah_klon_git,
        kedalaman_klon=kedalaman_klon,
    )

    ringkasan: dict[str, Any] = {
        "acara": ringkas["acara"],
        "nomor_build": ringkas["nomor_build"],
        "slug_pipa": ringkas["slug_pipa"],
        "slug_organisasi": ringkas["slug_organisasi"],
        "sumber_teks_pemindaian": sumber_teks,
        "anotasi_terkirim": False,
    }

    if not (teks_kode and teks_kode.strip()):
        ringkasan["peringatan"] = "tidak_ada_teks_untuk_dipindai"
        return ringkasan

    pesan_komit = str(ringkas.get("pesan_komit") or "")
    deteksi = deteksi_ai(
        teks_kode,
        pesan_commit=pesan_komit if pesan_komit.strip() else None,
        gunakan_llm=False,
        pengaturan=pengaturan,
    )
    analisis = analisis_kode(
        teks_kode,
        bahasa="python",
        apakah_ai=deteksi.apakah_ai,
        lewati_aturan_khusus_ai_jika_bukan_ai=True,
        pengaturan=pengaturan,
    )

    ringkasan["deteksi"] = {
        "apakah_ai": deteksi.apakah_ai,
        "skor_keyakinan": deteksi.skor_keyakinan,
    }
    ringkasan["analisis"] = {
        "jumlah_temuan": analisis.jumlah_temuan,
        "ringkasan_keparahan": analisis.ringkasan_keparahan(),
    }

    token_api = pengaturan.token_api_buildkite
    slug_org = (ringkas["slug_organisasi"] or pengaturan.slug_organisasi_buildkite or "").strip()
    slug_pipa = str(ringkas["slug_pipa"] or "").strip()
    nomor_mentah = ringkas["nomor_build"]
    try:
        nomor_build_int = int(nomor_mentah) if nomor_mentah is not None else None
    except (TypeError, ValueError):
        nomor_build_int = None

    if not token_api or not slug_org or not slug_pipa or nomor_build_int is None:
        ringkasan["anotasi"] = "dilewati_token_atau_metadata_tidak_lengkap"
        return ringkasan

    badan = _bangun_markdown_laporan(
        ringkas,
        deteksi,
        analisis,
        sumber_teks,
    )
    gaya = taksir_gaya_anotasi(analisis.daftar_temuan)

    try:
        ok, kode_http, teks = kirim_anotasi_build(
            token_api=token_api,
            slug_organisasi=slug_org,
            slug_pipa=slug_pipa,
            nomor_build=nomor_build_int,
            badan_markdown=badan,
            gaya=gaya,
            klien_http=klien_http,
        )
        ringkasan["anotasi_terkirim"] = ok
        ringkasan["anotasi_status_http"] = kode_http
        if not ok:
            ringkasan["anotasi_error"] = teks
    except Exception as exc:  # noqa: BLE001 — laporan aman ke klien webhook
        ringkasan["anotasi_terkirim"] = False
        ringkasan["anotasi_error"] = str(exc)[:400]

    return ringkasan


def _bangun_markdown_laporan(
    ringkas: dict[str, Any],
    deteksi: Any,
    analisis: Any,
    sumber_teks: str,
) -> str:
    """Membuat Markdown ringkas untuk panel Buildkite."""

    baris: list[str] = [
        "## GuardRail AI — hasil pemindaian",
        "",
        f"- **Build** #{ringkas.get('nomor_build')} — `{ringkas.get('status_build')}`",
        f"- **Pipeline** `{ringkas.get('slug_pipa')}`",
        f"- **Sumber teks:** {sumber_teks}",
        "",
        "### Deteksi AI",
        f"- `apakah_ai`: **{deteksi.apakah_ai}**",
        f"- `skor_keyakinan`: {deteksi.skor_keyakinan}",
        "",
        "### Analisis risiko",
        f"- **Jumlah temuan:** {analisis.jumlah_temuan}",
    ]
    ringkas_kep = analisis.ringkasan_keparahan()
    if ringkas_kep:
        cuplikan_keparahan = ", ".join(f"{k}: {v}" for k, v in ringkas_kep.items())
        baris.append(f"- **Per keparahan:** {cuplikan_keparahan}")

    if analisis.daftar_temuan:
        baris.extend(["", "**Contoh temuan (maks. 8):**", ""])
        for temuan in analisis.daftar_temuan[:8]:
            baris.append(
                f"- `{temuan.id_aturan}` ({temuan.tingkat_keparahan}) "
                f"L{temuan.nomor_baris or '?'} — {temuan.deskripsi[:120]}"
            )
    else:
        baris.extend(["", "_Tidak ada temuan aturan pada cuplikan ini._", ""])

    baris.append("")
    # Catatan: blok merge di pipeline (exit ≠ 0); webhook hanya untuk anotasi.
    baris.append(
        "_Webhook ini untuk anotasi; blok merge via langkah `guardrail` (exit non-zero)._"
    )
    return "\n".join(baris)
