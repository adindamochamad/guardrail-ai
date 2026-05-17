"""Pola regex yang sering muncul pada kode yang dihasilkan asisten AI (heuristik)."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DefinisiPola:
    """Satu pola teks dengan bobot kontribusi ke skor agregat."""

    nama: str
    pola_regex: re.Pattern[str]
    bobot_per_temuan: float
    kontribusi_maks: float


def daftar_pola_bawaan() -> list[DefinisiPola]:
    """Kumpulan pola awal; akan ditambah di iterasi hackathon."""

    return [
        DefinisiPola(
            nama="nama_variabel_generik",
            pola_regex=re.compile(
                r"\b(item|data|result|response|output|value|payload|temp)\b",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.07,
            kontribusi_maks=0.35,
        ),
        DefinisiPola(
            nama="nama_fungsi_generik",
            pola_regex=re.compile(
                r"def\s+(process|handle|execute|perform|validate|fetch)_[a-z0-9_]+\s*\(",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.12,
            kontribusi_maks=0.36,
        ),
        DefinisiPola(
            nama="try_except_umum_lalu_pass",
            pola_regex=re.compile(
                r"try\s*:.*?except\s+Exception\s*:\s*pass",
                re.IGNORECASE | re.DOTALL,
            ),
            bobot_per_temuan=0.25,
            kontribusi_maks=0.5,
        ),
        DefinisiPola(
            nama="komentar_berlebihan_berurutan",
            pola_regex=re.compile(r"(^\s*#.*\n){4,}", re.MULTILINE),
            bobot_per_temuan=0.2,
            kontribusi_maks=0.4,
        ),
        DefinisiPola(
            nama="placeholder_komentar_todo_ai",
            pola_regex=re.compile(
                r"#\s*(todo|fixme|note:\s*\(|NOTE:)",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.08,
            kontribusi_maks=0.24,
        ),
        DefinisiPola(
            nama="docstring_ringkas_generik",
            pola_regex=re.compile(
                r'"""[^"]{12,200}"""',
                re.DOTALL,
            ),
            bobot_per_temuan=0.06,
            kontribusi_maks=0.18,
        ),
        DefinisiPola(
            nama="f_string_sql_selector",
            pola_regex=re.compile(
                r"f[\"'].*SELECT\s+.+\s+FROM.+WHERE",
                re.IGNORECASE | re.DOTALL,
            ),
            bobot_per_temuan=0.18,
            kontribusi_maks=0.36,
        ),
        DefinisiPola(
            nama="subprocess_shell_true",
            pola_regex=re.compile(
                r"subprocess\.(run|call|Popen)\([^\)]*shell\s*=\s*True",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.1,
            kontribusi_maks=0.2,
        ),
        DefinisiPola(
            nama="os_system",
            pola_regex=re.compile(r"os\.system\s*\(", re.IGNORECASE),
            bobot_per_temuan=0.09,
            kontribusi_maks=0.18,
        ),
        DefinisiPola(
            nama="panggilan_eval",
            pola_regex=re.compile(r"\beval\s*\(", re.IGNORECASE),
            bobot_per_temuan=0.08,
            kontribusi_maks=0.16,
        ),
        DefinisiPola(
            nama="asyncio_run_puncak",
            pola_regex=re.compile(r"asyncio\.run\s*\(", re.IGNORECASE),
            bobot_per_temuan=0.07,
            kontribusi_maks=0.14,
        ),
        DefinisiPola(
            nama="main_guard_sederhana",
            pola_regex=re.compile(
                r'if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:\s*\n',
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.05,
            kontribusi_maks=0.15,
        ),
        DefinisiPola(
            nama="not_implemented_error",
            pola_regex=re.compile(r"raise\s+NotImplementedError\b", re.IGNORECASE),
            bobot_per_temuan=0.07,
            kontribusi_maks=0.14,
        ),
        DefinisiPola(
            nama="except_pass_ringkas",
            pola_regex=re.compile(r"except[^:\n]*:\s*pass", re.IGNORECASE),
            bobot_per_temuan=0.06,
            kontribusi_maks=0.18,
        ),
        DefinisiPola(
            nama="komentar_langkah_angka",
            pola_regex=re.compile(r"^\s*#\s*\d+\.\s", re.MULTILINE),
            bobot_per_temuan=0.05,
            kontribusi_maks=0.15,
        ),
        DefinisiPola(
            nama="getter_pendek_return_langsung",
            pola_regex=re.compile(
                r"def\s+get_[a-z0-9_]+\([^)]*\)\s*:\n\s+return\s+",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.05,
            kontribusi_maks=0.15,
        ),
        DefinisiPola(
            nama="default_arg_list_kosong",
            pola_regex=re.compile(r"def\s+[a-zA-Z0-9_]+\([^)]*=\s*\[\s*\]", re.IGNORECASE),
            bobot_per_temuan=0.08,
            kontribusi_maks=0.16,
        ),
        DefinisiPola(
            nama="hint_optional_union",
            pola_regex=re.compile(
                r"\b(Optional|Union)\[[^\]]+\]",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.03,
            kontribusi_maks=0.12,
        ),
        DefinisiPola(
            nama="komentar_jelaskan_param",
            pola_regex=re.compile(
                r"#\s*(Args|Arguments|Parameters|Params)\b",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.05,
            kontribusi_maks=0.15,
        ),
        DefinisiPola(
            nama="stub_lorem_ipsum_docstring",
            pola_regex=re.compile(
                r'"""\s*(lorem ipsum|example description)[^"]*"""',
                re.IGNORECASE | re.DOTALL,
            ),
            bobot_per_temuan=0.07,
            kontribusi_maks=0.14,
        ),
        DefinisiPola(
            nama="print_debug_kasar",
            pola_regex=re.compile(
                r"print\s*\(\s*[\"'](debug|dbg|trace)",
                re.IGNORECASE,
            ),
            bobot_per_temuan=0.04,
            kontribusi_maks=0.12,
        ),
    ]


def hitung_skor_pola(kode: str, pola_list: list[DefinisiPola] | None = None) -> tuple[float, dict]:
    """
    Menghitung skor 0–1 dari kecocokan pola. Ini bukti statistik, bukan klasifikator pasti.
    """

    if pola_list is None:
        pola_list = daftar_pola_bawaan()

    if not kode.strip():
        return 0.0, {"kecocokan": [], "keterangan": "kode_kosong"}

    total_baris = max(1, kode.count("\n") + 1)
    rincian: list[dict] = []
    akumulasi = 0.0

    for definisi in pola_list:
        jumlah = len(definisi.pola_regex.findall(kode))
        if jumlah == 0:
            continue
        kontribusi = min(
            definisi.kontribusi_maks,
            jumlah * definisi.bobot_per_temuan,
        )
        akumulasi += kontribusi
        rincian.append(
            {
                "nama": definisi.nama,
                "jumlah_temuan": jumlah,
                "kontribusi": round(kontribusi, 4),
            }
        )

    # Normalisasi lemah terhadap panjang agar file raksasa tidak selalu -> 1.0
    faktor_panjang = min(1.0, 80 / total_baris)
    skor_mentah = min(1.0, akumulasi * faktor_panjang)

    return skor_mentah, {
        "kecocokan": rincian,
        "jumlah_baris": total_baris,
        "faktor_panjang": round(faktor_panjang, 4),
    }
