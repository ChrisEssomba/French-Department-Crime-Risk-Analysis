# 🗺️ Crime Risk Mapping in France by Department

## 📌 Project Overview

As a soon-to-be graduate actively preparing for the job market, one of my key decision criteria when choosing a company is its location. Since I might have to live in the city where the company is based for several years, safety is a major concern.

To support this decision, I conducted a personal data analysis project using official data from the French Ministry of the Interior. The goal was to evaluate the crime risk across different departments in France, particularly those covering the cities I am considering: **Paris**, **Toulouse**, and **Lyon**.

This project combines **exploratory data analysis** and **interactive visualization** to display crime risk levels across France in the form of a dynamic map.

---

## 🗃️ Dataset

- **Source**: French Ministry of the Interior  
- **Content**: Crime and offense statistics recorded at the departmental level by the police and gendarmerie.
- **Period**: 2016–2024
- **Official link**: [data.gouv.fr dataset](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/)

---

## ❓ Problem Statement

> How can we build a map of France where each department is color-coded based on its crime index?

---

## 🎯 Objectives

1. Perform an **exploratory data analysis (EDA)** to understand the structure and key features of the dataset.
2. Analyze the data based on **five major crime categories** to compute an overall crime index per department.
3. Develop an interactive **Streamlit web application** that:
   - Visualizes crime risk across French departments using a geographic map.
   - Displays detailed crime statistics for a selected department.



## 📁 Project Structure

├── .devcontainer/               # Dev container configuration (optional)

├── dataset/

│   ├── data-dep.csv            # Raw departmental crime data

│   └── updated_data.csv        # Cleaned and processed dataset

│
├── departments.geojson         # GeoJSON file with department boundaries

├── main.ipynb                  # Jupyter Notebook for EDA

├── app.py                      # Streamlit web application

├── requirements.txt            # Python dependencies

└── README.md                   # Project documentation

---

## 🛠️ Technologies Used
- **Python (pandas, matplotlib, geopandas, plotly)**
- **Streamlit**
- **GeoJSON**
- **Jupyter Notebook**

    

    

## 🚀 How to Run the App

1. Create a virtual environment and install the dependencies:
   ```bash
   pip install -r requirements.txt

2. Launch the app from the terminal:
   ```bash
    streamlit run app.py
