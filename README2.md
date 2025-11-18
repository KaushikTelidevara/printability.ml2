📦 Printability Prediction Model

Machine-learning model to predict 3D print success probability (0–1) based on generative design features such as slenderness, base size, neck thickness, complexity, mass, overhang angle, and more.

This project trains and evaluates a Random Forest Regressor using a dataset of 20+ generatively designed brackets created in Fusion 360.
The goal is to build a tool that can estimate print success before manufacturing.

📁 Repository Structure
📂 printability.ml
 ├── printability_model.ipynb   # Jupyter Notebook with ML model
 ├── printable.csv              # Dataset used for training
 └── README.md                  # Project documentation

🧠 Project Overview

The dataset contains generative design outputs for 3D-printed brackets with variations in:

Base footprint

Neck thickness

Complexity

Slenderness ratio

Support mass / support volume

Overhang angle

Material usage

Print time

Safety factor / thickness

Stress results (Von Mises)

Each design is assigned a theoretical print success score between 0 and 1.

The ML model learns how geometric + printability features influence success probability.

📊 Machine Learning Model
Model:

✔ Random Forest Regressor
✔ Train/test split: 80/20
✔ Evaluation metrics: R², MAE

Results:

R² Score: ~0.85

Mean Absolute Error: ~0.095

This means the model explains 85% of the variance in print success — excellent for a small dataset.

🔍 Feature Importance (Top Predictors)
Feature	Importance
small_base_flag	0.2206
slenderness_ratio	0.1822
max_von_mises_mpa	0.1457
material_used_g	0.0744
volume_mm3	0.0741
mass_kg	0.0736
thin_neck_flag	0.0724
complexity_flag	0.0508

These trends match engineering intuition:

Small bases & slender shapes → unstable → lower success

High stress values → weaker prints

Complex geometry → harder to print

More material → more consistent printing

🧪 How to Run the Notebook
1. Create a conda environment (optional)
conda create -n printability_env python=3.10
conda activate printability_env

2. Install dependencies
pip install pandas numpy scikit-learn matplotlib

3. Launch Jupyter Notebook
jupyter notebook

4. Open the file

printability_model.ipynb

5. Run all cells

You will see:

Full dataset preview

Cleaned and processed features

Model training

R² and MAE outputs

Feature importance rankings

Prediction examples

📈 Example Prediction

Once trained, you can make predictions like:

model.predict([[small_base, thin_neck, complexity, ...]])

🌟 Future Improvements

Add more generative designs to increase dataset size

Export trained model as a .pkl file for future inference

Build a simple web UI tool (Streamlit)

Add STLs + screenshot thumbnails

Integrate print simulation metrics (overhang percentage, minimum feature size)

👤 Author

Kaushik Teiledvara
Mechanical Engineering — NUS
