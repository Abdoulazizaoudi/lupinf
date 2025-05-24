import streamlit as st
import numpy as np

# Titre de l'application
st.title("Prédiction du Risque Infectieux chez les Patients Lupiques 🔬")

# Sidebar pour les inputs utilisateur
with st.sidebar:
    st.header("Paramètres du Patient")
    eular = st.number_input("Score EULAR_ACR_2019", min_value=0, max_value=100, value=10)
    anti_ssb = st.selectbox("Anti-SSB", ["Positif", "Négatif"])
    vaccin = st.selectbox("Vaccin Pneumocoque", ["Non", "Oui"])
    prednisolone = st.selectbox("Traitement par Prednisolone", ["Non", "Oui"])

# Coefficients du modèle (issus de R)
COEFFICIENTS = {
    "intercept": -3.79107,
    "eular": 0.09395,
    "anti_ssb_positif": 1.77305,
    "vaccin_non": 4.35178,
    "prednisolone_non": 1.83229
}

# Fonction de calcul
def calculate_probability(eular, anti_ssb, vaccin, prednisolone):
    anti_ssb_num = 1 if anti_ssb == "Positif" else 0
    vaccin_num = 1 if vaccin == "Non" else 0
    prednisolone_num = 1 if prednisolone == "Non" else 0

    logit = (
        COEFFICIENTS["intercept"]
        + COEFFICIENTS["eular"] * eular
        + COEFFICIENTS["anti_ssb_positif"] * anti_ssb_num
        + COEFFICIENTS["vaccin_non"] * vaccin_num
        + COEFFICIENTS["prednisolone_non"] * prednisolone_num
    )

    probability = 1 / (1 + np.exp(-logit))
    return probability

# Bouton de prédiction
if st.button("Prédire"):
    prob = calculate_probability(eular, anti_ssb, vaccin, prednisolone)
    st.success(f"**Probabilité d'infection :** {prob * 100:.1f}%")

    # Interprétation simple selon seuil de 0.672
    if prob > 0.672:
        st.warning("Risque élevé d'infection.")
    else:
        st.info("Risque modéré ou faible d'infection.")

# Documentation
st.markdown("---")
st.markdown("""
**Instructions :**
1. Indiquez les caractéristiques du patient dans la barre latérale.
2. Cliquez sur *Prédire*.
3. La probabilité estimée d'infection et une interprétation s'afficheront ci-dessus.
""")
