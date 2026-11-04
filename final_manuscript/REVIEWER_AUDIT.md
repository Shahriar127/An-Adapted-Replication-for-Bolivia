# Reviewer-style audit of MANUSCRIPT.md

**Perspective:** a skeptical referee for a peer-reviewed development-economics or applied-ML journal. The audit was run on 2026-11-04 against the draft and its evidence files.

**Fixed during the audit:**
* **Gap widening.** The QRF–IRIS gap widening was stated as 0.034–0.061. The disjoint value recomputes to 0.067, so the range is now 0.034–0.067.
* **Threshold bounds.**
  * At 188.77 Bs the bound was ≤ 0.005; across all models it is ≤ 0.010.
  * At 189.05 Bs it was ≤ 0.002; it is ≤ 0.001.
  * For the training-sample line it was ≤ 0.011; it is ≤ 0.012.
* **Split count.** The A8 split count was stated as 30; it is 20.
* **Parameter count.** The linear model's parameters were stated as 22; the count is 29.
* **Abstract qualifiers.** "Single-split" qualifiers were added to the threshold-scan and forest-vs-tuning statements. They are the same in `ABSTRACT.md`.
* **Replication claims made more precise.**
  * Earlier project documents said the IRIS benchmark "replicates within the CI". In fact only BPAC and LE lie inside the published CIs; TA, PA and UC lie just outside.
  * The CV-QR quantile varies between 0.36 and 0.37 across iteration checkpoints. It is not fixed after 50 iterations.
* **Superseded figure.** The superseded "BPAC 0.797" figure, from the old TP+FP metric, is not used. The legacy-configuration result is reported under the published metrics instead: 0.784 vs 0.586.

**Automated numerical check:**
* `check_numbers.py` matched 358 decimal numbers in the manuscript against the evidence and published values.
* 11 were unmatched, and all were explained on manual review: configured threshold values, grid limits, section numbers, and a rounding of a published bound. See `number_check_report.txt` and `FINAL_CHECKLIST.md`.

## 1. Is the research question clear?
**Mostly.** The central question and the five sub-questions are explicit, and each is answered in its own subsection.

**Weakness:** the paper does two jobs at once, a replication and a sensitivity study. A reader may be unsure which is primary.

**Recommendation:** in the introduction, state that the replication *motivates* the sensitivity questions, and lead the results with the sensitivity findings for journals that publish method or robustness papers. **[Author decision.]**

## 2. Is the contribution supported by the experiments?

| Area | Assessment |
|---|---|
| Replication findings | Supported, with precise caveats: CV-QR close; IRIS partially; QRF not. |
| RQ1 (validation) | Supported by 30 splits per protocol. |
| RQ2 (quantile selection) | Supported. |
| RQ3 (thresholds) | Supported, partly single-split. |
| RQ4 (metric definitions) | Supported by direct recomputation. |
| RQ5 (forest vs tuning) | **Only partly supported.** The single-split evidence and the 3-split pilot point in different directions, and the manuscript says so. |
| Novelty | Moderate. Leakage and selection-bias effects are known in ML (Kaufman et al., 2012; Varma & Simon, 2006). Their size in a published PMT application, the BPAC algebra, and the replication audit are the new elements. |

## 3. Is the replication methodology transparent?
**Yes, and this is a strength.**
* There is a frozen methodology with page references, SPECIFIED, RECONSTRUCTED, ADAPTED and NOT IMPLEMENTED tags, and change control.
* Superseded results are archived with checksums.
* Unit tests check the published-table identities.
* The R source was inspected byte-level.

**Remaining opacity:** the welfare aggregate and the authors' code. Both are outside our control and are disclosed.

## 4. Are the metrics correctly defined and interpreted?
**Yes.**
* The published definitions are used throughout and verified against published numbers.
* The redundancy of PA and UC, and the piecewise form of BPAC, are derived and verified numerically.

**Caution:** the claim that BPAC "reduces to 1 − LE under over-prediction" is algebra. Its *practical* importance, i.e. leakage driving the rankings, depends on which regime the selected models fall in. The pilot and the quantile path confirm the regime for the cases examined, not in general.

## 5. Are the comparisons statistically justified?
**Partly. This is the main methodological weakness.**
* The primary comparisons rest on **one split (seed 42)** with test-sample bootstrap intervals. These do not reflect training or split variation, and the manuscript says so.
* The repeated-split analyses (30 splits) cover the frozen models. They **do not** cover CV-QR, whose 3-split pilot is too small for inference.
* Across-split dispersion is reported descriptively, with no corrected tests. That is appropriate given overlapping splits (Nadeau & Bengio, 2003), but it leaves the RQ5 comparison without a formal test.
* The threshold-scan counts (e.g. "38 of 82 lines") are not independent tests, and the manuscript labels them as descriptive.
* There is no multiplicity correction. No significance claims are made, so this is acceptable, but a referee may ask for one.

## 6. Are the claims stronger than the evidence?
After the fixes above, the claims are generally proportionate. Points to watch:
* **"Most of the QRF advantage … reflects the choice of quantile."** Supported on single splits: about 90% of the gap closes on the disjoint quantile path, and about 55% on the seed-42 published-protocol contrasts (CV − IRIS +0.037 against SE − IRIS +0.067). "Most" is borderline for the published protocol. **Consider "much of" or "a large share of".** [Author decision; the current text keeps "most" with a single-split qualifier.]
* **"Overlapping validation flatters flexible models."** The effect is measured. The *mechanism* (memorisation) is a hypothesis and is labelled as such in §6.
* **"Implementation is ruled out."** Ruled out for the factors tested and for the emulated R behaviour. A native R run was not performed, so state this as "emulated".

## 7. Are the limitations adequately disclosed?
**Yes.** The limitations table covers all the requested items and explains how each affects interpretation.

**Missing:** that the published PAT/BPAC framework is a specific institutional setting (USAID legislation), which limits external relevance. Briefly add this. **[Author decision.]**

## 8. Inconsistencies between tables, figures, abstract and conclusion
* The automated check passes (see above). The abstract, results and conclusion agree after the qualifier fixes.
* Figure 2 shows seed-42 results only. Its caption says so, and the text in §5.4 is consistent with it.
* **Note:** `RESULTS.md` §1 (frozen) contains the outdated sentence "candidate causes, none tested". The manuscript supersedes it. `FINAL_RESEARCH_ASSESSMENT.md` documents this.

## 9. Are the references authentic and relevant?
* 25 references were verified (Crossref, JMLR or CRAN). One has its end page flagged (Koenker & Bassett, 1978).
* 4 are taken from the published article's reference list and not re-verified: Grosh & Baker 1995; IRIS 2005; Schreiner 2006; Meinshausen 2016.
* No citation was invented. Two candidates were dropped (Alderman 2002: DOI not resolvable; FGT 1984: not needed).
* **Gap (updated in Step 3):** a targeted Crossref/OpenAlex search (`REFERENCES.md` §C) added 16 verified references, including PMT error reviews, ML-PMT studies, leakage and poverty-line literature. The gap statement is now phrased as the result of a non-systematic search. No study on poverty-line sensitivity in ML-PMT evaluation was found; poverty-measurement work is cited as an analogy only. A systematic search remains advisable.
* **Relevance:** improved. PMT inclusion and exclusion errors are now covered by Devereux et al. (2017), and ML-PMT by Sohnesen & Stender (2017), Poulin et al. (2022) and Wobcke & Mariyah (2023). One possibly important item remains unverified: a 2015 working paper on PMT accuracy for Bolivia (`REFERENCES.md` §B).

## 10. Three biggest reasons a reviewer might reject

1. **The replication is incomplete at its most interesting point (A8).** The published QRF result is not reproduced, the welfare variable differs, and the cause is unidentified. A referee may argue that every comparison with the published forest is uninterpretable, and that the paper therefore reports results on a different dataset construction.
2. **Thin statistical evidence for the key substantive question (RQ5).** The forest-vs-tuning conclusion rests on one split per protocol and a 3-split pilot that points the other way, with no formal across-split inference. A referee may ask for the planned repeated-split CV-QR comparison (about 4–5 hours of compute for 10 splits per protocol).
3. **Limited scope and novelty.** One 2005 survey from one country, and a method critique whose ingredients (leakage, selection bias, calibration of the quantile) are individually known. A referee may judge the contribution incremental without a second country or a more general framework.

**Possible mitigations, without new experiments:**
* frame the paper explicitly as a replication and robustness note;
* foreground the BPAC algebra and the reporting inconsistencies as general lessons;
* state RQ5 as open;
* target a venue that publishes replications.

**Mitigations needing work (your decision):**
* the repeated CV-QR comparison (ready to run: `audit_2026-11-04_repeated_split/`);
* contacting the authors about A8.

## Verdict
The manuscript is **ready for supervisor review**, not yet for journal submission. Outstanding before submission:
* the literature search (research gap and threshold literature);
* the Koenker & Bassett end page;
* the author decisions flagged above;
* trimming the abstract to the target journal's limit (currently about 400 words);
* the RQ5 evidence decision.
