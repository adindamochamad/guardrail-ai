"""Model SQLAlchemy untuk penyimpanan scan, berkas, deteksi AI, dan risiko."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import BasisModel


class Scan(BasisModel):
    """Satu proses pemindaian (batch atau tunggal) terhadap satu atau banyak berkas."""

    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dibuat_pada: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime,
        default=lambda: datetime.now(UTC),
    )
    sumber: Mapped[str | None] = mapped_column("source", String(128), nullable=True)
    payload_tambahan: Mapped[dict[str, Any] | None] = mapped_column(
        "extra_json",
        JSON,
        nullable=True,
    )

    daftar_berkas: Mapped[list[CodeFile]] = relationship(
        back_populates="scan_induk",
        cascade="all, delete-orphan",
    )


class CodeFile(BasisModel):
    """Berkas kode yang menjadi subjek analisis."""

    __tablename__ = "code_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_scan: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("scans.id", ondelete="CASCADE"),
        index=True,
    )
    path_berkas: Mapped[str] = mapped_column("path", String(1024))
    hash_konten: Mapped[str | None] = mapped_column(
        "content_hash",
        String(64),
        nullable=True,
    )

    scan_induk: Mapped[Scan] = relationship(back_populates="daftar_berkas")
    deteksi_ai: Mapped[AIDetection | None] = relationship(
        back_populates="berkas_kode",
        cascade="all, delete-orphan",
        uselist=False,
    )
    daftar_risiko: Mapped[list[Risk]] = relationship(
        back_populates="berkas_kode",
        cascade="all, delete-orphan",
    )


class AIDetection(BasisModel):
    """Hasil deteksi apakah cuplikan/berkas berkemungkinan berasal dari AI."""

    __tablename__ = "ai_detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_berkas_kode: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("code_files.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    apakah_ai: Mapped[bool | None] = mapped_column("is_ai", Boolean, nullable=True)
    skor_keyakinan: Mapped[float | None] = mapped_column(
        "confidence",
        Float,
        nullable=True,
    )
    sinyal: Mapped[dict[str, Any] | None] = mapped_column(
        "signals",
        JSON,
        nullable=True,
    )

    berkas_kode: Mapped[CodeFile] = relationship(back_populates="deteksi_ai")


class Risk(BasisModel):
    """Satu temuan risiko terikat ke sebuah berkas kode."""

    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_berkas_kode: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("code_files.id", ondelete="CASCADE"),
        index=True,
    )
    id_aturan: Mapped[str] = mapped_column("rule_id", String(64))
    tingkat_keparahan: Mapped[str] = mapped_column("severity", String(32))
    nomor_baris: Mapped[int | None] = mapped_column(
        "line_number",
        Integer,
        nullable=True,
    )
    deskripsi: Mapped[str] = mapped_column("description", Text)
    saran_perbaikan: Mapped[str | None] = mapped_column(
        "fix_hint",
        Text,
        nullable=True,
    )

    berkas_kode: Mapped[CodeFile] = relationship(back_populates="daftar_risiko")
