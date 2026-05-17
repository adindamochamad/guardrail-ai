"""Definisi aturan regex (lingkup universal / Python / JavaScript)."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class AturanRegex:
    """Aturan berbasis pencocokan teks."""

    id_aturan: str
    kategori: str
    tingkat_keparahan: str
    pola: re.Pattern[str]
    deskripsi: str
    saran_perbaikan: str | None
    khusus_ai: bool
    lingkup: str  # universal | python | javascript


def daftar_aturan_regex_bawaan() -> list[AturanRegex]:
    """Kumpulan aturan Day 3; akan ditambah sesuai roadmap (50+)."""

    return [
        AturanRegex(
            id_aturan="GR_SEC_SQL_FMT_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(
                r"f[\"'][^\"']*(SELECT|INSERT|UPDATE|DELETE)[^\"']*\{",
                re.IGNORECASE,
            ),
            deskripsi="Kemungkinan SQL dibentuk dengan f-string/interpolasi — risiko injeksi.",
            saran_perbaikan=(
                "Gunakan kueri berparameter / ORM; "
                "jangan menyisipkan variabel mentah ke SQL."
            ),
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_SQL_CONCAT_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(
                r"\+\s*[\"'][^\"']*(SELECT|INSERT|UPDATE|DELETE)",
                re.IGNORECASE,
            ),
            deskripsi="Kemungkinan SQL dibangun dengan konkatenasi string.",
            saran_perbaikan="Gunakan parameter terikat atau query builder.",
            khusus_ai=False,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_AKSES_AWS_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
            deskripsi="Potensi access key AWS tertanam di kode.",
            saran_perbaikan="Pakai secret manager / env; rotasi kunci yang terpapar.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_API_KEY_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(
                r"(api[_-]?key|apikey|secret)\s*=\s*[\"'][^\"'\\s]{12,}[\"']",
                re.IGNORECASE,
            ),
            deskripsi="Kemungkinan kunci atau rahasia hardcoded.",
            saran_perbaikan="Pindahkan ke variabel lingkungan atau penyimpanan rahasia.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_PASSWORD_LITERAL_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(
                r"(password|passwd|pwd)\s*=\s*[\"'][^\"']{4,}[\"']",
                re.IGNORECASE,
            ),
            deskripsi="Kata sandi atau token mirip sandi dalam literal string.",
            saran_perbaikan="Gunakan otentikasi terkelola; jangan hardcode kredensial.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_PEM_PRIVATE_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            deskripsi="Potensi kunci privat PEM di dalam berkas.",
            saran_perbaikan="Hapus dari repo; gunakan HSM / secret vault; rotasi kunci.",
            khusus_ai=False,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_SUBPROC_SHELL_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(
                r"subprocess\.(run|call|Popen)\([^\)]*shell\s*=\s*True",
                re.IGNORECASE,
            ),
            deskripsi="Subprocess dengan shell=True meningkatkan risiko injeksi perintah.",
            saran_perbaikan="Hindari shell=True; gunakan daftar argumen dan shell=False.",
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_OS_SYSTEM_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(r"os\.system\s*\(", re.IGNORECASE),
            deskripsi="os.system memudahkan injeksi perintah.",
            saran_perbaikan="Gunakan subprocess dengan argumen lista, tanpa shell.",
            khusus_ai=False,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_EVAL_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(r"\beval\s*\(", re.IGNORECASE),
            deskripsi="eval dapat mengeksekusi kode arbitrer.",
            saran_perbaikan="Hindari eval; gunakan parser/serializer yang aman.",
            khusus_ai=False,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_EXEC_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(r"\bexec\s*\(", re.IGNORECASE),
            deskripsi="exec membuka pintu eksekusi dinamis berbahaya.",
            saran_perbaikan="Refaktor agar tidak perlu exec.",
            khusus_ai=False,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_PICKLE_LOADS_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(r"pickle\.loads?\s*\(", re.IGNORECASE),
            deskripsi="Unpickle data tidak tepercaya dapat menjalankan kode.",
            saran_perbaikan=(
                "Jangan unpickle dari sumber tidak tepercaya; "
                "pertimbangkan JSON/protobuf."
            ),
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_YAML_LOAD_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(r"yaml\.load\s*\(\s*[^,\)]+\s*\)", re.IGNORECASE),
            deskripsi="yaml.load tanpa Loader aman berisiko eksekusi tag.",
            saran_perbaikan="Gunakan yaml.safe_load atau Loader eksplisit yang aman.",
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_SSL_VERIFY_FALSE_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(r"verify\s*=\s*False", re.IGNORECASE),
            deskripsi="Mematikan verifikasi TLS membuka MITM.",
            saran_perbaikan="Gunakan verify=True dan rantai sertifikat yang benar.",
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_DEBUG_TRUE_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(
                r"(app\.run\s*\(\s*debug\s*=\s*True|DEBUG\s*=\s*True)",
                re.IGNORECASE,
            ),
            deskripsi="Mode debug sering membocorkan informasi di produksi.",
            saran_perbaikan="Matikan debug di lingkungan produksi; gunakan konfigurasi per env.",
            khusus_ai=False,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_CORS_WILDCARD_001",
            kategori="security",
            tingkat_keparahan="MEDIUM",
            pola=re.compile(
                r"(Access-Control-Allow-Origin|CORS).*[\"']\s*\*",
                re.IGNORECASE,
            ),
            deskripsi="CORS wildcard bisa memperluas permukaan serangan.",
            saran_perbaikan="Batasi origin spesifik yang dipercaya.",
            khusus_ai=False,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_CHMOD_777_001",
            kategori="security",
            tingkat_keparahan="MEDIUM",
            pola=re.compile(r"chmod\s+['\"]?777|0o777|0+777\b"),
            deskripsi="Izin berkas terlalu terbuka (777).",
            saran_perbaikan="Gunakan least privilege.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_HTTP_LITERAL_001",
            kategori="security",
            tingkat_keparahan="LOW",
            pola=re.compile(r"[\"']http://(?!localhost|127\.0\.0\.1)[^\"']+[\"']"),
            deskripsi="URL http:// jelas (bukan TLS).",
            saran_perbaikan="Utamakan https:// atau domain dengan TLS.",
            khusus_ai=False,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_JWT_NONE_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(r"[\"']none[\"']\s*,\s*[^)]*verify\s*=\s*False", re.IGNORECASE),
            deskripsi="Pola yang mengingatkan pada JWT alg=none / verifikasi mati.",
            saran_perbaikan="Verifikasi tanda tangan dan algoritma secara eksplisit.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_PRIV_LOGGING_SENSITIVE_001",
            kategori="compliance",
            tingkat_keparahan="MEDIUM",
            pola=re.compile(
                r"(print|logger\.|logging\.)\([^\)]*(password|token|ssn|secret)",
                re.IGNORECASE,
            ),
            deskripsi="Log atau print memuat kata kunci data sensitif.",
            saran_perbaikan="Masking/redaksi; patuhi kebijakan privasi.",
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_LIC_GPL_PASTE_001",
            kategori="compliance",
            tingkat_keparahan="LOW",
            pola=re.compile(r"GNU GENERAL PUBLIC LICENSE", re.IGNORECASE),
            deskripsi="Cuplikan teks lisensi GPL di dalam kode — tinjau legalitas penyalinan.",
            saran_perbaikan="Pastikan kepatuhan lisensi dependensi/salindia.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_LOGIC_BARE_EXCEPT_001",
            kategori="logic",
            tingkat_keparahan="MEDIUM",
            pola=re.compile(r"except\s*:\s*\n\s*(pass|continue)", re.IGNORECASE),
            deskripsi="except tanpa tipe menelan error dan menyulitkan debugging.",
            saran_perbaikan="Tangkap pengecualian spesifik; re-raise atau log.",
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_LOGIC_EXC_PASS_001",
            kategori="logic",
            tingkat_keparahan="LOW",
            pola=re.compile(r"except\s+Exception\s*:\s*pass", re.IGNORECASE),
            deskripsi="Menelan Exception secara diam-diam.",
            saran_perbaikan="Log minimal atau tangani secara eksplisit.",
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_PERF_N_PLUS_1_HINT_001",
            kategori="performance",
            tingkat_keparahan="LOW",
            pola=re.compile(
                r"for\s+\w+\s+in\s+.+\s*:\s*\n\s+.*\.objects?\.(get|filter)\(",
                re.IGNORECASE,
            ),
            deskripsi="Poling yang mengingatkan pada pola N+1 ORM.",
            saran_perbaikan="Gunakan select_related / prefetch / batch query.",
            khusus_ai=True,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_JS_INNERHTML_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(
                r"\.innerHTML\s*=",
                re.IGNORECASE,
            ),
            deskripsi="Penetapan innerHTML rentan XSS.",
            saran_perbaikan="Gunakan textContent atau sanitasi tepercaya.",
            khusus_ai=True,
            lingkup="javascript",
        ),
        AturanRegex(
            id_aturan="GR_JS_DANGEROUS_HTML_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(r"dangerouslySetInnerHTML", re.IGNORECASE),
            deskripsi="dangerouslySetInnerHTML memerlukan sanitasi ketat.",
            saran_perbaikan="Hindari HTML mentah; gunakan library sanitasi.",
            khusus_ai=True,
            lingkup="javascript",
        ),
        AturanRegex(
            id_aturan="GR_JS_EVAL_001",
            kategori="security",
            tingkat_keparahan="CRITICAL",
            pola=re.compile(r"\beval\s*\(", re.IGNORECASE),
            deskripsi="eval di JavaScript berisiko tinggi.",
            saran_perbaikan="Hindari eval; parse JSON dengan JSON.parse.",
            khusus_ai=False,
            lingkup="javascript",
        ),
        AturanRegex(
            id_aturan="GR_JS_NEW_FUNCTION_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(r"new\s+Function\s*\(", re.IGNORECASE),
            deskripsi="Function konstruktor mirip eval.",
            saran_perbaikan="Hindari konstruksi fungsi dinamis dari string.",
            khusus_ai=True,
            lingkup="javascript",
        ),
        AturanRegex(
            id_aturan="GR_SEC_CMD_INJECTION_CHAIN_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(r"shell\s*=\s*True", re.IGNORECASE),
            deskripsi="shell=True pada subprocess (duplikat lintas-konteks).",
            saran_perbaikan="Matikan shell; gunakan argv list.",
            khusus_ai=False,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_SEC_RANDOM_SECRET_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(
                r"(SECRET_KEY|JWT_SECRET)\s*=\s*[\"'][^\"']{1,64}[\"']",
                re.IGNORECASE,
            ),
            deskripsi="Secret key statik pendek atau hardcoded.",
            saran_perbaikan="Gunakan secret panjang acak dari env/secret manager.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_TOKEN_BEARER_HARDCODED_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(
                r"Authorization[\"']?\s*[:=]\s*[\"']Bearer\s+[A-Za-z0-9_\-\.]{20,}",
                re.IGNORECASE,
            ),
            deskripsi="Token Bearer lengkap tampak hardcoded.",
            saran_perbaikan="Ambil token dari penyimpanan aman saat runtime.",
            khusus_ai=True,
            lingkup="universal",
        ),
        AturanRegex(
            id_aturan="GR_SEC_SQL_EXEC_RAW_001",
            kategori="security",
            tingkat_keparahan="HIGH",
            pola=re.compile(
                r"\.execute\s*\(\s*[\"'][^\"']*(SELECT|INSERT|UPDATE|DELETE)",
                re.IGNORECASE,
            ),
            deskripsi="execute() dengan string SQL literal — periksa parameterisasi.",
            saran_perbaikan="Gunakan placeholder parameter.",
            khusus_ai=False,
            lingkup="python",
        ),
        AturanRegex(
            id_aturan="GR_PERF_SLEEP_IN_LOOP_001",
            kategori="performance",
            tingkat_keparahan="LOW",
            pola=re.compile(
                r"for\s+.+\s*:\s*\n\s+.*time\.sleep\s*\(",
                re.IGNORECASE,
            ),
            deskripsi="time.sleep dalam loop bisa menurunkan throughput.",
            saran_perbaikan="Pertimbangkan async/backoff terstruktur.",
            khusus_ai=True,
            lingkup="python",
        ),
    ]


def filter_aturan_oleh_lingkup(
    aturan: list[AturanRegex],
    bahasa: str,
) -> list[AturanRegex]:
    """Memilih aturan regex yang relevan untuk bahasa sumber."""

    bahasa_normal = bahasa.strip().lower()
    if bahasa_normal in {"py", "python"}:
        lingkup_diijinkan = {"python", "universal"}
    elif bahasa_normal in {"js", "javascript", "ts", "typescript"}:
        lingkup_diijinkan = {"javascript", "universal"}
    else:
        lingkup_diijinkan = {"universal"}

    return [a for a in aturan if a.lingkup in lingkup_diijinkan]
