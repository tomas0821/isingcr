# Conversion notes — marker Mode A (`--disable_ocr`)

All 16 references in `NOVELTY_CHECK.md` §3 converted 2026-08-16 from PDFs manually
attached to the Zotero items (Sociophysics ▸ IsingCR collection). Mode A = text/table
layer only, no OCR, no LaTeX for equations (per `pdf-to-markdown` skill defaults) — the
right choice here since none of these are scanned PDFs (all have real, substantial text
layers) and none of the physics content this project needs from them is equation-heavy
enough to justify Mode B's ~100x runtime cost.

Two more converted 2026-08-19, same Mode A settings: `godoylorite2020` (Godoy-Lorite &
Jones 2020, arXiv:2003.07146 — downloaded directly from arXiv rather than via Zotero
storage sync, which hadn't propagated the file yet) and `okamoto2021` (Okamoto 2021,
10.1038/s41598-021-03050-z, from nature.com). Both are `NOVELTY_CHECK.md` §2b/§3
adjacent-but-not-colliding references, **not cited in the manuscript** — filed for
completeness only. Spot-checked against `pdftotext -layout`: negative signs and numeric
values in both papers' surviving tables reproduce correctly (e.g. okamoto2021's
"N_seat=60", "⌈60/8⌉=7"; godoylorite2020's table of per-election regression coefficients
including negative values like -0.333, -0.491).

**Fidelity spot-check (korbel2026, siegenfeld2020):** numeric values, units, and signs
verified against `pdftotext -layout` on the source PDF — all correct (e.g. korbel2026's
`T* = 0.922`, `hc = $1.83M`, `∼1.8 million USD` all reproduced exactly).

## Known losses — table bodies dropped, captions survived

Mode A's documented failure mode (per the `pdf-to-markdown` skill): a table can be
*detected* (counted in marker's "tables_total") but fail to *extract* structurally
("tables_pdftext"), in which case the caption/title/notes around it survive as prose but
the actual data rows are silently absent. Checked systematically across all 16 (compared
each paper's `tables_total` vs. `tables_pdftext` from the run log against actual
markdown-table line counts); four papers have a **complete** loss of at least one table:

| Paper | Table | What's missing |
|---|---|---|
| `korbel2026` | TABLE I (confusion table), TABLE II (McNemar contingency table), **TABLE III (summary of estimated T\*, hc, and accuracy per decade)** | All 3 captions present (lines 305, 311, 335), all 3 bodies absent. **TABLE III is the highest-value loss in this batch** — it's a real numeric result (per-decade fitted parameters), not just a supporting table. |
| `tiwari2021` | Table 1 (conformist-agent model parameters), Table 2 (conformist+contrarian model parameters) | Both captions present (lines 113, 135), both bodies absent — parameter/symbol glossaries, lower stakes than korbel2026's loss but still worth having if this paper's parameter conventions matter for comparison. |
| `cascantematamoros2006` | Tabla 1 (electoral calendar, abstention averages, and territorial-distribution index averages by year, 1953–2016) | Caption, title, and footnote all present (lines 83–88), body absent. |
| `dibenedetto2023` | Table E.2 (transition thresholds, appendix) | Caption present, body absent — appendix table, low stakes. |

**Partial losses** (some but not all detected tables extracted; the markdown does contain
*some* real table content for these, just not 100%) — not individually itemized here,
flagged generically per the skill's guidance rather than hand-verified table-by-table:

| Paper | Detected | Extracted |
|---|---|---|
| `massoli2026` | 14 | 11 |
| `mitra2026` | 10 | 8 |
| `cardoso2023` | 2 | 1 |
| `chavarriamora2022` | 3 | 2 |
| `camachosanchez2025` | 2 | 1 |
| `godoylorite2020` | 3 | 2 |

**No table loss** (either no tables detected, or detected count matches extracted count):
`braha2017`, `galam2021`, `jordan2020`, `mullick2025`, `raducha2025`, `siegenfeld2020`,
`cardoso2022` (1/1), `okamoto2021` (1/1).

## If a missing table matters

Re-run just that paper's conversion in Mode B (`--highres_image_dpi 400`, needs the CUDA
llama-server env vars — see the `pdf-to-markdown` skill) — the vision-OCR path can
recover table structure Mode A's pdftext-only extraction misses, at the cost of ~2 min
per paper on this machine and the equation/small-glyph caveats documented in that skill
(leading spin-arrow misreads, multi-tier header fragmentation). `korbel2026`'s TABLE III
is the one candidate in this batch actually worth that re-run if its per-decade numbers
end up cited.
