# Submission checklist (final, 2026-11-06)

Replaces `FINAL_CHECKLIST.md` (2026-11-04). Legend: [x] done and verified · [ ] **you must supply** · [!] default chosen, change it if you disagree.

## Ready-to-submit files (`final_manuscript/submission/`)
| File | Content |
|---|---|
| `Manuscript.docx` / `.pdf` | **Typeset in the format of the reference article (WBER / OUP house style; measured specification in `CODE_REVIEW.md` §6):** 7 × 10 in page, Garamond 9.5/12.45 pt body, Roman-numeral sections, author note as first-page footnote, running heads, tables and figures in house style, 47 Chicago author-date references. 18 pages. |
| `Online_Appendix.docx` / `.pdf` | A: frozen methodology; B: claim–evidence table; C: literature-search log; D: supplementary Tables S1–S6 |
| `Figure1_threshold_scan.pdf/.png`, `Figure2_quantile_path.pdf/.png` | Separate figure files at print width: vector PDF and 600-dpi PNG |

Rebuild after any edit to the Markdown: `python3 final_manuscript/build_docs.py` (then re-run `extract_numbers.py`, `check_numbers.py`, `tables/make_tables.py`; figures: `figures/make_journal_figures.py`).

## Done and verified
- [x] Frozen pipeline and the shorter audits re-run from raw data and reproduce byte-for-byte (`CODE_REVIEW.md`).
- [x] 23/23 unit tests; raw-data checksums; published values in the code match the article PDF.
- [x] Number check: 487 decimal numbers in the body, 16 unmatched, all explained. Wrong number fixed (3.0–9.6 → 3.0–10.0).
- [x] **2015 working paper now cited** (McBride & Nichols, 2015; verified via the IHSN citation catalogue) in §3.4, §5.5 and §6.6.
- [x] **Klasen & Lange (2015)**, the Bolivia PMT-accuracy paper, verified via RePEc and added to §2 (described from its abstract only).
- [x] Data citation for EH 2005 (Instituto Nacional de Estadística, 2005) added and cited in §3.1.
- [x] Reference list pasted into the manuscript (47 entries; every entry cited and every citation listed).
- [x] Internal file names in the text replaced by Online Appendix A–C references.
- [x] Abstract cut from 387 to 237 words.
- [x] Institutional specificity of PAT/BPAC (US legislative mandate, p. 533) added to the Limitations table.
- [x] Figures: journal versions without embedded title or footer; that text is now in the captions.
- [x] Pipeline run time corrected; `threshold_scan_family_ranking.csv` now has a generating script.

## Defaults I chose (change if you disagree)
- [!] **"Much of"** instead of "most" for the quantile-choice claim (abstract, §5.6, §8, claim M14). This was the safer wording recommended by the self-audit. The previous text is in `versions/MANUSCRIPT_v4_2026-11-06_after_final_review.md`.
- [!] **RQ5 stated as open** (no new 10-split run). Running it would take about 4–5 hours per protocol with `audit_2026-11-04_repeated_split/scripts/repeated_split_cvqr_vs_qrf.py`.
- [!] **Code licence: MIT** (`LICENSE`), excluding the INE data and the GPL R excerpts. Replace it if your institution requires another licence.
- [!] **Title:** option 1. Alternatives: *How Robust Are Machine-Learning Gains in Poverty Targeting? A Replication and Sensitivity Analysis with Bolivian Household Data*; *Retooling Revisited: An Adapted Replication of Machine-Learning Proxy Means Tests for Bolivia*.
- [x] **Format follows the reference article (2026-11-07):** Chicago author-date citations and references, one-paragraph abstract, JEL classification + key words, unnumbered introduction, Roman-numeral sections, figures in the text with captions above, figures renumbered by first citation (Figure 1 = threshold scan).
- [!] **Fonts:** Sabon and Univers are commercial; the DOCX uses Garamond / Arial / Arial Narrow, and the PDF uses the free equivalents EB Garamond / Liberation Sans. If you own Sabon and Univers, change `SERIF`/`SANS` in `build_docs.py` and rebuild.
- [!] **Abstract length:** 237 words. The reference article's abstract is about 130 words. If you target WBER, check its current limit and shorten if needed.
- [!] Many journals (including WBER) want the *submitted* manuscript double-spaced; the typeset look matches the published article as you asked. To get a double-spaced review copy, set the body leading in `build_docs.py` to 24 pt.

## You must supply (placeholders in the manuscript)
- [x] **Authors (2026-11-07):** Md. Shahriar Jubair Mahim (first and corresponding author, shahriarjubair27@gmail.com), Abdullah Al Masud, A S M Delowar Hossain. Also in `LICENSE` and `CITATION.cff`.
- [!] **Supervisor listed as third (last) author**, the usual position for a supervisor. If he should instead be acknowledged only, move him to the Acknowledgements and remove him from the byline, `LICENSE` and `CITATION.cff`.
- [!] **Affiliation assumed the same for all three authors:** Department of CSE, MBSTU, Tangail, Bangladesh. Correct it if a co-author has a different affiliation.
- [ ] **Funding and acknowledgements** (Declarations). Competing interests are pre-filled as "none", marked [Confirm.]; confirm or edit.
- [x] **Repository URL** inserted in "Data and code availability" (2026-11-07): https://github.com/Shahriar127/An-Adapted-Replication-for-Bolivia
- [ ] **Make the repository public** before submission (it is private, so reviewers would get a 404). Optional: archive a tagged release on Zenodo and add the DOI.
- [ ] **Target journal**, then check its word limit (body about 8,000 words), citation style and figure rules.
- [ ] Confirm the **INE Bolivia data terms** if the journal's data editor asks.
- [ ] A **cover letter** (journal-specific).
- [ ] Optional: a supervisor or co-author read-through of `Manuscript.pdf`.

## Strongest likely reviewer objections (from `REVIEWER_AUDIT.md` §10)
1. A8 is unresolved: the published forest result is not reproduced, and the cause is unknown.
2. RQ5 rests on one split per protocol plus a 3-split pilot.
3. One country, one 2005 survey; the individual ingredients (leakage, selection bias) are known.

How the paper already mitigates them: it is framed as a replication and robustness study, states RQ5 as open, and documents every discrepancy. Prefer a venue that publishes replications.
