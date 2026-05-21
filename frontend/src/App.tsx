import { useMemo, useState } from 'react'

/** Respons cuplikan deteksi dari API */
interface BalasanDeteksi {
  apakah_ai: boolean
  skor_keyakinan: number
  ambang_batas: number
  sinyal: Record<string, unknown>
}

/** Satu temuan analisis */
interface TemuanAnalisis {
  id_aturan: string
  kategori: string
  tingkat_keparahan: string
  nomor_baris: number | null
  deskripsi: string
  saran_perbaikan?: string | null
  cuplikan?: string | null
  dari_ast: boolean
}

interface BalasanAnalisis {
  daftar_temuan: TemuanAnalisis[]
  jumlah_temuan: number
  ringkasan_keparahan: Record<string, number>
  apakah_ai_inferensi: boolean
  apakah_ai_efektif: boolean
  bahasa: string
}

interface BalasanPindaian {
  deteksi: BalasanDeteksi
  analisis: BalasanAnalisis
  jumlah_total_aturan_sistem: number
}

const contohKodeAwal = `import os
kata_sandi = "rahasia-123"

def jalankan():
    # Contoh pola berisiko: eval dari input pengguna
    eval(input("perintah: "))
`

/** Map warna badge untuk tingkat keparahan bawaan backend */
function kelasBadgeKeparahan(tingkat: string): string {
  const n = tingkat.toUpperCase()
  if (n === 'CRITICAL') return 'bg-rose-500/20 text-rose-200 ring-rose-500/40'
  if (n === 'HIGH') return 'bg-orange-500/20 text-orange-200 ring-orange-500/40'
  if (n === 'MEDIUM') return 'bg-amber-500/20 text-amber-100 ring-amber-500/35'
  if (n === 'LOW') return 'bg-slate-600/40 text-slate-300 ring-slate-500/40'
  return 'bg-slate-700/50 text-slate-300 ring-slate-600/50'
}

/** Basis URL API — env build-time atau fallback produksi */
function dapatkanBasisApi(): string {
  const dariEnv = import.meta.env.VITE_API_BASE_URL?.trim()
  if (dariEnv) return dariEnv.replace(/\/$/, '')
  return 'https://guardrail-api.adindamochamad.com'
}

function App() {
  const [teksKode, setTeksKode] = useState(contohKodeAwal)
  const [bahasaPilihan, setBahasaPilihan] = useState('python')
  const [gunakanLlm, setGunakanLlm] = useState(false)
  const [sedangMemuat, setSedangMemuat] = useState(false)
  const [pesanGalat, setPesanGalat] = useState<string | null>(null)
  const [hasilPindaian, setHasilPindaian] = useState<BalasanPindaian | null>(null)

  const basisApi = useMemo(() => dapatkanBasisApi(), [])
  const tautanDocs = `${basisApi}/docs`

  const ringkasanUntukBatang = useMemo(() => {
    if (!hasilPindaian) return []
    const urutanKunci: readonly string[] = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    const peta = hasilPindaian.analisis.ringkasan_keparahan
    const nilaiMaks = Math.max(1, ...urutanKunci.map((k) => peta[k] ?? 0))
    return urutanKunci.map((kunci) => ({
      kunci,
      jumlah: peta[kunci] ?? 0,
      persen: Math.round(((peta[kunci] ?? 0) / nilaiMaks) * 100),
    }))
  }, [hasilPindaian])

  async function kirimPindaian(): Promise<void> {
    setPesanGalat(null)
    setSedangMemuat(true)
    setHasilPindaian(null)
    try {
      const badan = {
        kode: teksKode,
        pesan_commit: null,
        gunakan_llm: gunakanLlm,
        bahasa: bahasaPilihan,
        apakah_ai: null,
        lewati_aturan_khusus_ai_jika_bukan_ai: true,
      }
      const resp = await fetch(`${basisApi}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(badan),
      })
      if (!resp.ok) {
        let detail = resp.statusText
        try {
          const errJson = (await resp.json()) as { detail?: unknown }
          if (errJson.detail !== undefined) {
            detail = JSON.stringify(errJson.detail)
          }
        } catch {
          /* parse error boleh diabaikan */
        }
        throw new Error(`HTTP ${resp.status}: ${detail}`)
      }
      const data = (await resp.json()) as BalasanPindaian
      setHasilPindaian(data)
    } catch (kesalahan) {
      const teks = kesalahan instanceof Error ? kesalahan.message : 'Permintaan gagal'
      setPesanGalat(teks)
    } finally {
      setSedangMemuat(false)
    }
  }

  return (
    <div className="min-h-svh bg-[radial-gradient(ellipse_120%_80%_at_50%_-20%,rgba(16,185,129,0.18),transparent)]">
      <header className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-400/90">
              DevNet AI+ML Hackathon 2026
            </p>
            <h1 className="mt-1 text-2xl font-semibold tracking-tight text-white sm:text-3xl">
              GuardRail AI
            </h1>
            <p className="mt-2 max-w-xl text-sm leading-relaxed text-slate-400">
              Dashboard pemindaian: deteksi jejak AI pada kode lalu analisis risiko (regex + AST) dalam satu
              alur.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <a
              href={tautanDocs}
              target="_blank"
              rel="noreferrer"
              className="rounded-lg border border-slate-600 bg-slate-900/50 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-emerald-500/50 hover:text-white"
            >
              Buka Swagger
            </a>
            <button
              type="button"
              onClick={() => setTeksKode(contohKodeAwal)}
              className="rounded-lg border border-slate-600 bg-slate-900/50 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-slate-500"
            >
              Muat contoh kode
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-6xl gap-8 px-4 py-8 lg:grid-cols-[1fr,minmax(0,1.1fr)]">
        <section className="space-y-4 rounded-2xl border border-slate-800 bg-slate-900/40 p-5 shadow-xl shadow-black/20 backdrop-blur-sm">
          <h2 className="text-lg font-semibold text-white">Kode</h2>
          <textarea
            value={teksKode}
            onChange={(e) => setTeksKode(e.target.value)}
            spellCheck={false}
            className="h-72 w-full resize-y rounded-xl border border-slate-700 bg-slate-950/80 p-4 font-mono text-sm leading-relaxed text-emerald-100/95 outline-none ring-emerald-500/0 transition focus:border-emerald-500/50 focus:ring-2 focus:ring-emerald-500/25"
            placeholder="Tempel cuplikan kode di sini…"
          />

          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div className="flex flex-wrap gap-4">
              <label className="block text-sm">
                <span className="mb-1 block text-slate-500">Bahasa</span>
                <select
                  value={bahasaPilihan}
                  onChange={(e) => setBahasaPilihan(e.target.value)}
                  className="rounded-lg border border-slate-600 bg-slate-950 px-3 py-2 text-sm text-slate-200 outline-none focus:border-emerald-500/60"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                  <option value="text">Universal (teks)</option>
                </select>
              </label>
              <label className="flex cursor-pointer items-center gap-2 pt-6 text-sm text-slate-300">
                <input
                  type="checkbox"
                  checked={gunakanLlm}
                  onChange={(e) => setGunakanLlm(e.target.checked)}
                  className="size-4 rounded border-slate-500 bg-slate-900 text-emerald-500 focus:ring-emerald-500/40"
                />
                Gunakan LLM (butuh{' '}
                <code className="rounded bg-slate-800 px-1">OPENAI_API_KEY</code>)
              </label>
            </div>
            <button
              type="button"
              disabled={sedangMemuat || !teksKode.trim()}
              onClick={() => void kirimPindaian()}
              className="rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-900/30 transition hover:from-emerald-500 hover:to-teal-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {sedangMemuat ? 'Memindai…' : 'Jalankan pemindaian'}
            </button>
          </div>

          <p className="text-xs text-slate-500">
            API: <span className="font-mono text-slate-400">{basisApi}</span>
          </p>
        </section>

        <section className="space-y-4">
          {pesanGalat && (
            <div
              role="alert"
              className="rounded-2xl border border-rose-500/40 bg-rose-950/40 px-4 py-3 text-sm text-rose-100"
            >
              {pesanGalat}
            </div>
          )}

          {!hasilPindaian && !pesanGalat && !sedangMemuat && (
            <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-900/20 p-8 text-center text-slate-500">
              Hasil deteksi dan analisis akan tampil di sini setelah Anda menjalankan pemindaian.
            </div>
          )}

          {hasilPindaian && (
            <>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-5">
                  <h3 className="text-sm font-medium uppercase tracking-wide text-slate-500">Deteksi AI</h3>
                  <div className="mt-3 flex flex-wrap items-center gap-3">
                    <span
                      className={`rounded-full px-3 py-1 text-sm font-semibold ring-1 ${
                        hasilPindaian.deteksi.apakah_ai
                          ? 'bg-violet-500/20 text-violet-200 ring-violet-500/40'
                          : 'bg-slate-600/40 text-slate-200 ring-slate-500/40'
                      }`}
                    >
                      {hasilPindaian.deteksi.apakah_ai ? 'Indikasi AI' : 'Cenderung manusia'}
                    </span>
                    <span className="text-sm text-slate-400">
                      Skor {(hasilPindaian.deteksi.skor_keyakinan * 100).toFixed(1)}% · ambang{' '}
                      {(hasilPindaian.deteksi.ambang_batas * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all"
                      style={{
                        width: `${Math.min(100, hasilPindaian.deteksi.skor_keyakinan * 100)}%`,
                      }}
                    />
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-5">
                  <h3 className="text-sm font-medium uppercase tracking-wide text-slate-500">Analisis</h3>
                  <p className="mt-2 text-2xl font-semibold text-white">
                    {hasilPindaian.analisis.jumlah_temuan}{' '}
                    <span className="text-base font-normal text-slate-400">temuan</span>
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    Aturan sistem: {hasilPindaian.jumlah_total_aturan_sistem} · Bahasa:{' '}
                    {hasilPindaian.analisis.bahasa}
                  </p>
                </div>
              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5">
                <h3 className="text-sm font-medium text-slate-400">Distribusi keparahan</h3>
                <div className="mt-4 flex h-28 items-end gap-2">
                  {ringkasanUntukBatang.map(({ kunci, jumlah, persen }) => (
                    <div key={kunci} className="flex flex-1 flex-col items-center gap-2">
                      <div
                        className="w-full max-w-[3.5rem] rounded-t-md bg-gradient-to-t from-slate-800 to-emerald-600/90 transition-all"
                        style={{ height: `${Math.max(8, persen)}%` }}
                        title={`${kunci}: ${jumlah}`}
                      />
                      <span className="text-center text-[10px] font-medium uppercase text-slate-500">
                        {kunci.slice(0, 3)}
                      </span>
                      <span className="text-xs font-semibold text-slate-300">{jumlah}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/40">
                <div className="border-b border-slate-800 px-4 py-3">
                  <h3 className="text-sm font-semibold text-white">Daftar temuan</h3>
                </div>
                <div className="max-h-[28rem] overflow-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="sticky top-0 bg-slate-900/95 text-xs uppercase text-slate-500 backdrop-blur">
                      <tr>
                        <th className="px-4 py-3 font-medium">Keparahan</th>
                        <th className="px-4 py-3 font-medium">Aturan</th>
                        <th className="px-4 py-3 font-medium">Baris</th>
                        <th className="px-4 py-3 font-medium">Deskripsi</th>
                        <th className="px-4 py-3 font-medium">AST</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/80">
                      {hasilPindaian.analisis.daftar_temuan.map((temuan, indeks) => (
                        <tr
                          key={`${temuan.id_aturan}-${indeks}`}
                          className="bg-slate-950/20 hover:bg-slate-800/30"
                        >
                          <td className="whitespace-nowrap px-4 py-3 align-top">
                            <span
                              className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ${kelasBadgeKeparahan(temuan.tingkat_keparahan)}`}
                            >
                              {temuan.tingkat_keparahan}
                            </span>
                          </td>
                          <td className="px-4 py-3 align-top font-mono text-xs text-emerald-200/90">
                            {temuan.id_aturan}
                          </td>
                          <td className="px-4 py-3 align-top text-slate-400">
                            {temuan.nomor_baris ?? '—'}
                          </td>
                          <td className="px-4 py-3 align-top text-slate-300">
                            <p>{temuan.deskripsi}</p>
                            {temuan.saran_perbaikan && (
                              <p className="mt-1 text-xs text-slate-500">
                                Saran: {temuan.saran_perbaikan}
                              </p>
                            )}
                          </td>
                          <td className="px-4 py-3 align-top text-slate-500">
                            {temuan.dari_ast ? 'Ya' : ''}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </section>
      </main>

      <footer className="border-t border-slate-800/80 py-8 text-center text-xs text-slate-600">
        GuardRail AI · deteksi + analisis risiko untuk kode berbasis AI
      </footer>
    </div>
  )
}

export default App
