# Predicting FDM printability of generative-design brackets

A workflow that joins Fusion 360 generative design, Bambu Studio slicer data and a Random Forest model to score how printable each bracket design is, then picks a design that balances mass, stress and printability.

Solo term project for ME3261 Computer-Aided Design and Manufacturing, National University of Singapore (Aug–Nov 2025). Full write-up with figures and physical print results: **[kaushiktelidevara.com/printability](https://kaushiktelidevara.com/printability.html)**

## Summary

- **20 designs:** 19 Fusion 360 generative-design outcomes plus one hand-modelled baseline, all for the same bracket load case.
- **Slicer data:** each design sliced in Bambu Studio for a Bambu Lab A1 Mini (default PLA settings, supports on) to record support mass and volume, print time and material used.
- **Printability score:** each design scored 0.1–1.0 from three geometric risk flags (small base, thin neck, complexity) and its slicer preview.
- **Model:** Random Forest regressor (scikit-learn, 200 trees) on 15 numeric features, 70/30 split. R² 0.85, MAE 0.095 on the 6 held-out designs.
- **Selection:** a weighted index across mass, volume, peak stress and printability picked a 19 g design over both the 65 g baseline and the 9 g lightest design.
- **Physical check:** four designs printed in PLA; outcomes matched their printability scores.

**Caveat:** the printability score is partly derived from the same risk flags that are model inputs, so the R² mostly reflects that scoring rule. The useful result is which measurable features carry the signal: base size, slenderness and peak stress, rather than the generative-design settings. A real predictor would need labels from repeated physical prints and flags measured automatically from geometry.

## Repository

```
printable.csv           Dataset: 20 designs x 15 numeric features + print_success
printability.ipynb      Notebook with the full workflow
src/model_training.py   Standalone script: trains the model, prints R² and MAE, saves plots
environment.yml         Conda environment
```

## Run it

With conda:

```bash
git clone https://github.com/KaushikTelidevara/printability.ml2.git
cd printability.ml2
conda env create -f environment.yml
conda activate printability_env
python src/model_training.py
```

Or with pip:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn jupyter
python src/model_training.py
```

The script prints R² and MAE and saves `feature_importance.png` and `actual_vs_pred.png`. To step through the analysis instead, run `jupyter notebook` and open `printability.ipynb`.

## Dataset

| Group | Columns |
|---|---|
| Generative-design inputs | `gd_safety_factor`, `gd_min_thickness_mm`, `max_overhang_angle`, `gd_unrestricted_flag` (1 = unrestricted, 0 = manufacturing-aware) |
| Solver results | `max_von_mises_mpa`, `mass_kg`, `volume_mm3` |
| Slicer results | `support_mass_g`, `support_volume_ml`, `estimated_print_time_min`, `material_used_g` |
| Geometry and risk flags | `slenderness_ratio`, `small_base_flag`, `thin_neck_flag`, `complexity_flag` |
| Target | `print_success`, a printability score from 0.1 to 1.0 |

## Results

Most important features: small-base flag (0.22), slenderness ratio (0.18) and peak von Mises stress (0.15). Safety factor, minimum thickness and the unrestricted flag rank lowest, so the final geometry matters more than the settings that produced it.

Selection index, each term min–max normalised across the 20 designs:

```
0.30 × (1 − mass) + 0.20 × (1 − volume) + 0.25 × (1 − stress) + 0.25 × printability
```

Top design: `GD_Unrestricted_2_1` at 0.82 (19 g, 20 MPa, printability 0.75). The baseline scores 0.49 and the 9 g design 0.55.

## Tools

Fusion 360 generative design, Bambu Studio, Python (pandas, scikit-learn, matplotlib, seaborn), Jupyter.
