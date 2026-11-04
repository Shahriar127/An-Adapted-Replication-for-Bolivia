# Final checklist: Bolivia PMT manuscript (2026-11-04)

Legend: [x] done and verified · [ ] open · [!] needs your decision.

## Reproducibility
- [x] **Frozen methodology unchanged** (`METHODOLOGY_REFERENCE.md`, `common.py`). The pre-audit SHA-256 snapshot verifies 121 of 121 files (`audit_2026-11-04_repeated_split/logs/PRE_AUDIT_CHECKSUMS.sha256`). No file in `results/` or `archive/` is newer than the snapshot.
- [x] **Reproducibility package untouched** (`../reproducibility_package_2026-11-03.tar.gz`; included in the snapshot).
- [x] **Unit tests pass:** 23 of 23, `python3 -m unittest discover -s tests`, run after writing.
- [x] **Every manuscript number is regenerated read-only** from existing outputs by `final_manuscript/extract_numbers.py` into `evidence_numbers.csv` (586 values).
- [x] **Figures are byte-identical copies** of the Step 5 outputs (SHA-256 matched).
- [x] **Run instructions:** `run_all.sh` (frozen pipeline), `run_audits.sh` (A8, CV-QR, Table A2), and the Step 5 and pilot scripts in their `audit_*` directories, each with a run log.
- [ ] **Raw data licence and formal data citation:** confirm with INE Bolivia before publication.
- [ ] **Code and data availability statement:** decide on the public repository and licence for the code.

## Numerical consistency
- [x] `final_manuscript/check_numbers.py` (re-run after Step 4): 484 decimal numbers checked, 16 unmatched, all explained on manual review:
  - 0.374: published UC lower bound 37.35% rounded half-up.
  - 0.99: quantile-grid limit.
  - 170.0, 177.5, 189.05, 194.10, 94.55, 378.18 (and 174.5, registered as derived): configured threshold values in the threshold-scan, sensitivity and Table A2 scripts.
  - 3.1, 4.5, 5.1, 6.2, 6.3, 6.4: section numbers.
  - 3.14, 1.17: software versions (Python 3.14.8, SciPy 1.17.1; from `ENVIRONMENT.txt`).
- [x] Errors found and corrected in the draft (see `REVIEWER_AUDIT.md`): the gap-widening range, threshold-effect bounds, the A8 split count, the parameter count, the share of the gap closed, and the abstract qualifiers.
- [x] The abstract (`ABSTRACT.md`) is identical to the manuscript abstract.
- [x] Superseded numbers (old TP+FP metric, archive, "0.797") are not used.
- [ ] Re-run `check_numbers.py` after any edit to `MANUSCRIPT.md`.

## Claims
- [x] Every major claim is mapped to its evidence and type in `CLAIM_EVIDENCE_TABLE.md`.
- [x] Hypotheses are labelled as hypotheses: A8 cause (R12), overlap mechanism (M16). The forest-beyond-tuning claim (M15) is "not established".
- [x] No claim that QRF outperforms the published method or linear QR.
- [!] "Most of the QRF advantage … reflects quantile choice" is borderline for the published protocol (about 55%). Consider "much of". (`REVIEWER_AUDIT.md` §6)

## Citations
- [x] APA 7th edition throughout `REFERENCES.md`.
- [x] 25 references verified (Crossref API, JMLR BibTeX, CRAN).
- [x] 4 references taken from the published article's reference list and labelled as such.
- [x] No invented references. 2 candidates excluded with reasons.
- [x] Koenker & Bassett (1978): end page 50 confirmed via RePEc (Step 3).
- [x] **Literature search (Step 3, targeted, non-systematic):** (a) gap statement rephrased as a search result; (b) poverty-line sensitivity: none found for ML-PMT, analogy to Atkinson (1987) and Ravallion & Bidani (1994); (c) PMT error literature added (Devereux et al., 2017). No **[verify]** markers remain in the manuscript. 44 references in `REFERENCES.md` §A, all cited.
- [ ] Verify and read the 2015 Bolivia PMT working paper found in the search (`REFERENCES.md` §B); a systematic search is advisable before submission.
- [x] **Discussion (Step 4):** rewritten as §§6.1–6.8, answering why overlap helps forests, why test-set selection is optimistic, why rankings are stable across lines, and why A8 is unresolved, each with an evidence status. New supporting values were added read-only to `extract_numbers.py` (`disc|*` keys) and to `CLAIM_EVIDENCE_TABLE.md` (M17–M22, R14).
- [ ] Length: about 8,250 words after Steps 3–4. Check the target journal's limit; §6 and §4 are the easiest to shorten.
- [ ] Convert in-text citations to the target journal's style if it is not APA.

## Manuscript completion
- [x] Title options, with one selected.
- [x] Abstract, Introduction, Related Work, Data and Methodology, Experimental Setup, Results, Discussion, Limitations, Conclusion, Data and code availability, figure captions.
- [x] Step 2 (2026-11-04): restructured into 10 parts (Abstract, §1 Introduction, §2 Related Work, §3 Data and Methodology, §4 Experimental Setup, §5 Results, §6 Discussion, §7 Limitations, §8 Conclusion, References). Section references updated in `CLAIM_EVIDENCE_TABLE.md`, `REVIEWER_AUDIT.md` and this file. Previous version kept in `versions/MANUSCRIPT_v1_2026-11-04_before_restructure.md`.
- [x] Adaptations and differences from the published study documented (§3.5).
- [ ] Abstract length: about 400 words. Trim to the target journal's limit.
- [ ] Figures: check that the resolution and format meet the journal's requirements. Current PNGs are 200 dpi.
- [!] Framing: replication-first or sensitivity-first. (`REVIEWER_AUDIT.md` §1)
- [!] Add a sentence on the institutional specificity of PAT/BPAC. (`REVIEWER_AUDIT.md` §7)
- [!] RQ5 evidence: submit with RQ5 stated as open, or first run the prepared 10-split CV-QR comparison (about 4–5 hours per protocol). (`REVIEWER_AUDIT.md` §10)
- [ ] Supervisor review.
- [ ] Choose the target venue. **[Verify scope; no venue has been assessed.]**

## Status
**Ready for supervisor review.** Not yet ready for journal submission. See the open items above.
