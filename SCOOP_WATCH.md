# SCOOP_WATCH — IsingCR

Re-runs of the queries recorded in `NOVELTY_CHECK.md` §2–§2f. Only hits absent from
§3/§4/§5 and from `manuscript/references.bib` are logged. This file never edits
`NOVELTY_CHECK.md`; proposed additions are noted and left for the author to apply.

## 2026-10-18 — 4 new: 0 collision, 0 narrows, 4 adjacent
Queries re-run: 5 (§2 `check_novelty.py`, verbatim) + 4 FastTrack (1 duplication test,
3 searches) on the two claims that postdate §2f. Connector: available. 56 days since
§2d, the pre-submission gate named in §5 — this run satisfies it.

- Achitouv, Chavalarias & Lahoche, "Inferring the microscopic mechanisms of opinion
  dynamics using a kinetic Ising model" — arXiv 2026 — arXiv:2609.23690 — ADJACENT.
  Kinetic Ising inferred from a year of real online-network data; external field read as
  intrinsic bias, coupling as social influence; MC on the empirical temporal network
  reproduces response functions and flip probabilities. Closest new work on empirically
  fitting a field/coupling decomposition. Not a collision: online social network, not
  geography; no election returns; no resolution comparison.
- Lo Sasso, "Shannon entropy and complex network community detection to study electoral
  coalition behaviour at municipal scale" — arXiv 2026 — arXiv:2609.18200 — ADJACENT.
  Statistical physics and network theory on polling-section returns in Bari. Network
  built from vote-expression correlations, not border adjacency — the same
  differentiation as Elmakais & Glickman and Michaud et al. in §2e. Argues explicitly
  that these models are rarely applied to local-level data, which supports §4.1's
  motivation rather than threatening it.
- Caldarelli, Artime, Fischetti et al., "The physics of news, rumors, and opinions" —
  Physics Reports 2026 — 10.1016/j.physrep.2026.05.002 — ADJACENT. Flagship review of
  statistical physics of opinion dynamics, spin models included. Propose adding to §3
  and citing alongside `mullick2025`: a 2026 Physics Reports review of exactly this
  framework is one a Physica A referee may expect to see.
- Sivak, Cantrell, Emery et al., "Births are difficult to predict even with rich survey
  and full-population register data" — arXiv 2026 — arXiv:2609.01194 — ADJACENT, optional.
  Independent use of the same methodological move as the sign-agreement ceiling: estimate
  a predictive ceiling, then read observed performance against it. Different field, so
  citation is optional.

**Positioning risk, not a new hit.** The duplication test on the snapshot-versus-time-average
claim returned the classical Ising metastability literature: Stoll & Schneider (1972),
Capocaccia, Cassandro & Olivieri (1974), McCraw & Schulman (1978), Davies (1982), Shteto,
Boukheddaden & Varret (1999), Lipowski & Johnston (2000), Cirillo & Nardi (2003), De Smedt,
Godrèche & Luck (2003), Stariolo & Cugliandolo (2019) — the last proposing trapping regions
defined by purely dynamical criteria. None concerns elections or a fit to data, so none is a
collision. But §4.7 currently presents the metastable-versus-trapping distinction as a
contribution, and this is settled statistical mechanics that a Physica A readership knows.
Recommend reframing the claim as transferring a standard distinction to the data-fitting
practice of this literature, with one or two of these cited.

Known hits the DOI diff surfaced that are already recorded in §3 by arXiv ID (so the
published DOI did not match): Elmakais & Glickman (Israeli cantons), Devauchelle, Szymczak
& Nowakowski (tight elections). Not new.

Noise: 38 of 39 DOIs returned by the §2 keyword queries were query artifacts of the
bag-of-words behaviour documented in §2's traps (book chapters, BSI standards, PeerJ
supplements, a 1982 PhysRevB paper, SSRN, unrelated quantum-computing preprints).

Verified in passing: `korbel2026` → 10.1103/9gjj-1df6 and `fernandezgracia2014` →
10.1103/PhysRevLett.112.158701 both confirmed exact against Crossref (authors, title,
volume, issue, pages, year).
