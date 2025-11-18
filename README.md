🧩 Predicting 3D Printability Using Generative Design & Machine Learning

This project integrates generative design, 3D printing slicing data, and machine learning to predict the printability of parts produced using Bambu Lab printers.

The work forms part of a CAD/CAM assignment requiring:

 Data collection from Generative Design (Fusion 360)
 Slicer output from Bambu Studio
 Printability labelling
 A machine learning model predicting print success
 A well-documented GitHub repository containing code, data, environment files, and instructions

🔍 1. Project Overview

3D printing success depends heavily on geometric features such as base size, slenderness, wall thickness, neck thickness, and overhang angles.
To explore this relationship, we generated 20 variations of a bracket using Autodesk Fusion 360's Generative Design engine, varying:

 Safety factor
 Minimum thickness
 Overhang constraints
 Unrestricted vs. manufacturing-aware settings
 Base geometry
 Neck thickness
 Complexity

Each design was sliced in Bambu Studio, which produced additional print-related features:

 Support volume
 Support mass
 Print time
 Material usage

Finally, each design was assigned a print_success score (0–1) based on theoretical assessment of:

 Small base stability
 Thin neck failure risk
 Complexity & overhang difficulty

This dataset was used to train a Random Forest regressor that predicts printability.

📁 2. Repository Structure
printability.ml/
│
├── printable.csv                 # Full dataset
├── printability_model.ipynb      # Jupyter Notebook (full workflow)
├── src/
│   ├── model_training.py         # Clean standalone ML script
│
├── environment.yml               # Conda environment for reproducibility
├── .gitignore                    # Ignore cache files / ipynb checkpoints
└── README.md                     # Project documentation

⚙️ 3. Installation
✔ Option A — Using Conda (recommended)
conda env create -f environment.yml
conda activate printability_env

✔ Option B — Manual Install
pip install numpy pandas scikit-learn matplotlib jupyter seaborn

🧪 4. Running the Machine Learning Model
✔ Option A — Run the Notebook

Open the Jupyter notebook:
jupyter notebook

Then open:
printability_model.ipynb

✔ Option B — Run the Script Directly
python src/model_training.py

This will:

 Train the Random Forest model
 Print model accuracy (R², MAE)
 Save visualizations:
  feature_importance.png
  actual_vs_pred.png

📊 5. Dataset Description

The dataset contains 20 rows (20 generative designs) and the following key features:

Generative Design Inputs
Feature	Description
gd_safety_factor	Safety factor used in GD
gd_min_thickness_mm	Min wall thickness constraint
max_overhang_angle	Allowable overhang angle
gd_unrestricted_flag	1 = unrestricted, 0 = manufacturing-aware
max_von_mises_mpa	GD stress result
Print Geometry
Feature	Description
mass_kg	Part mass
volume_mm3	Part volume
slenderness_ratio	Height / base footprint
Printability Risk Factors
Feature	Meaning
small_base_flag	0 = stable, 1 = small unstable base
thin_neck_flag	0 = very thin weak neck, 1 = thick strong neck
complexity_flag	0 = simple, 1 = highly complex

🎯 Target Variable
print_success — a continuous score (0–1) estimating theoretical print success.

🤖 6. Machine Learning Model

A Random Forest Regressor was used due to:

 Small dataset
 Non-linear relationships
 Ability to extract feature importance

Performance

R² Score: ~0.85
MAE: ~0.09

This means the model predicts printability with good accuracy, especially considering the dataset size.

🔬 7. Feature Importance (Insights)

The model identified these as the strongest predictors:

Rank	Feature	Influence
1	small_base_flag - Very strong (base stability is critical)
2	slenderness_ratio - Tall slender parts are risky
3	max_von_mises_mpa	- Stress distribution matters
4	material_used_g	- Related to mass/dimensions
5	volume_mm3 -	Size & geometry effects
...	...	lower influence

This aligns well with 3D-printing domain knowledge.

🖼️ 8. Visual Outputs

Once you run the script, you will get:

✔ feature_importance.png

A ranked bar chart of which parameters most affect print success.

✔ actual_vs_pred.png

A scatter plot showing prediction vs. ground truth.

📦 9. Reproducibility

Anyone can reproduce the results by:

git clone https://github.com/KaushikTeiledvara/printability.ml.git
cd printability.ml
conda env create -f environment.yml
conda activate printability_env
python src/model_training.py

🏁 10. Conclusion

This project successfully integrates:

Autodesk Generative Design
Bambu Studio slicing outputs
Hand-labelled printability metrics
Random Forest regression

The model demonstrates strong predictive power and provides actionable insights into what geometric factors most strongly influence FDM print success.

This workflow can be extended with:

More data (physical print tests)
Expanded GD design space
Neural networks or gradient boosting models
