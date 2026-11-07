# Place the raw Bolivia EH 2005 files here

This folder is intentionally empty. The INE Bolivia microdata are not redistributed.

1. Download `EH2005.rar` from <https://siip.produccion.gob.bo/repSIIP2/files/encuesta_hogares/EH2005.rar>.
2. Extract it, then put these files in this folder:
   * `EH2005.rar`
   * `BASE_EH_2005_(Pob_y_Viv).sav`
   * `Bolivia_Equipamiento.sav`
   * `Bolivia_Pecuaria.sav`
3. From the package root, run `sha256sum -c SHA256SUMS`. All four files must report `OK`. If a hash differs, INE has changed the files, and results may differ.

See `../../DATASET.md` for the full description.
