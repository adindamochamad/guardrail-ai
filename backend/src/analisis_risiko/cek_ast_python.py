"""Pemeriksaan semantik ringan lewat AST untuk Python."""

from __future__ import annotations

import ast

from .tipe_data import TemuanRisiko


def temuan_dari_ast_python(pohon: ast.AST) -> list[TemuanRisiko]:
    """Mengumpulkan temuan struktural yang sulit ditangkap regex saja."""

    pengunjung = _PengunjungBahaya()
    pengunjung.visit(pohon)
    return pengunjung.temuan


class _PengunjungBahaya(ast.NodeVisitor):
    """Mencatat pola panggilan berisiko umum di kode Python."""

    def __init__(self) -> None:
        self.temuan: list[TemuanRisiko] = []

    def visit_Call(self, node: ast.Call) -> None:
        self._periksa_panggilan(node)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        # Asersi bisa dimatikan dengan -O; hindari untuk invariant kritis.
        self.temuan.append(
            TemuanRisiko(
                id_aturan="GR_AST_LOGIC_ASSERT_001",
                kategori="logic",
                tingkat_keparahan="LOW",
                nomor_baris=node.lineno,
                deskripsi="Pernyataan assert — dioptimasi dapat dilewati (python -O).",
                saran_perbaikan="Validasi eksplisit + pengecualian untuk invariant penting.",
                cuplikan=None,
                dari_ast=True,
            )
        )
        self.generic_visit(node)

    def _periksa_panggilan(self, node: ast.Call) -> None:
        baris = node.lineno

        if isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                self._tambah(
                    "GR_AST_EVAL_001",
                    "security",
                    "CRITICAL",
                    baris,
                    "Panggilan eval() terdeteksi.",
                    "Hindari eval; gunakan parser aman.",
                )
            elif node.func.id == "exec":
                self._tambah(
                    "GR_AST_EXEC_001",
                    "security",
                    "CRITICAL",
                    baris,
                    "Panggilan exec() terdeteksi.",
                    "Hindari exec untuk input dinamis.",
                )
            elif node.func.id == "compile":
                self._tambah(
                    "GR_AST_COMPILE_001",
                    "security",
                    "HIGH",
                    baris,
                    "compile() dinamis dapat dipakai untuk kode arbitrer.",
                    "Kurangi penggunaan compile dari string tidak tepercaya.",
                )
            elif node.func.id == "__import__":
                self._tambah(
                    "GR_AST_DUNDER_IMPORT_001",
                    "security",
                    "MEDIUM",
                    baris,
                    "Panggilan __import__ dinamis.",
                    "Periksa allow-list modul sebelum impor dinamis.",
                )

        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "system":
                if self._adalah_modul(node.func.value, "os"):
                    self._tambah(
                        "GR_AST_OS_SYSTEM_001",
                        "security",
                        "HIGH",
                        baris,
                        "os.system dipanggil.",
                        "Gunakan subprocess tanpa shell.",
                    )
            elif node.func.attr in {"loads", "load"}:
                if self._adalah_modul(node.func.value, "pickle"):
                    self._tambah(
                        "GR_AST_PICKLE_001",
                        "security",
                        "CRITICAL",
                        baris,
                        "pickle.load(s) pada data tidak tepercaya berbahaya.",
                        "Ganti dengan format serialisasi aman.",
                    )
            elif node.func.attr == "md5":
                if self._adalah_modul(node.func.value, "hashlib"):
                    self._tambah(
                        "GR_AST_HASH_MD5_001",
                        "security",
                        "MEDIUM",
                        baris,
                        "hashlib.md5 — hash lemah untuk konteks keamanan.",
                        "Gunakan sha256 atau primitif kripto modern.",
                    )
            elif node.func.attr == "mktemp":
                if self._adalah_modul(node.func.value, "tempfile"):
                    self._tambah(
                        "GR_AST_MKTEMP_001",
                        "security",
                        "MEDIUM",
                        baris,
                        "tempfile.mktemp rentan race condition.",
                        "Gunakan NamedTemporaryFile / mkstemp.",
                    )
            elif node.func.attr == "load":
                if self._adalah_modul(node.func.value, "yaml"):
                    self._tambah(
                        "GR_AST_YAML_LOAD_AST_001",
                        "security",
                        "HIGH",
                        baris,
                        "yaml.load — pastikan Loader aman.",
                        "Gunakan safe_load bila memungkinkan.",
                    )
            elif node.func.attr in {"run", "call", "Popen"}:
                if self._adalah_subprocess(node.func.value):
                    if self._keyword_shell_true(node):
                        self._tambah(
                            "GR_AST_SUBPROCESS_SHELL_001",
                            "security",
                            "CRITICAL",
                            baris,
                            "subprocess dipanggil dengan shell=True.",
                            "Set shell=False dan gunakan daftar argumen.",
                        )

    def _keyword_shell_true(self, node: ast.Call) -> bool:
        for kw in node.keywords:
            if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                return True
        return False

    def _adalah_modul(self, value: ast.expr, nama_modul: str) -> bool:
        return isinstance(value, ast.Name) and value.id == nama_modul

    def _adalah_subprocess(self, value: ast.expr) -> bool:
        return isinstance(value, ast.Name) and value.id == "subprocess"

    def _tambah(
        self,
        id_aturan: str,
        kategori: str,
        tingkat: str,
        baris: int,
        deskripsi: str,
        saran: str,
    ) -> None:
        self.temuan.append(
            TemuanRisiko(
                id_aturan=id_aturan,
                kategori=kategori,
                tingkat_keparahan=tingkat,
                nomor_baris=baris,
                deskripsi=deskripsi,
                saran_perbaikan=saran,
                cuplikan=None,
                dari_ast=True,
            )
        )


def jumlah_pemeriksaan_ast_bawaan() -> int:
    """Jumlah aturan AST bawaan (untuk asersi tes roadmap)."""

    return 11
