/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Basis URL API GuardRail (tanpa slash akhir) */
  readonly VITE_API_BASE_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
