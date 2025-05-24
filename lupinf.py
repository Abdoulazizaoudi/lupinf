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

# Coefficients du modèle issus de R
COEFFICIENTS = {
    "intercept": -3.77041,
    "eular": 0.12574,
    "anti_ssb_positif": 2.00572,
    "vaccin_non": 3.99037
}

# Fonction de calcul de la probabilité
def calculate_probability(eular, anti_ssb, vaccin):
    anti_ssb_num = 1 if anti_ssb == "Positif" else 0
    vaccin_num = 1 if vaccin == "Non" else 0

    logit = (
        COEFFICIENTS["intercept"]
        + COEFFICIENTS["eular"] * eular
        + COEFFICIENTS["anti_ssb_positif"] * anti_ssb_num
        + COEFFICIENTS["vaccin_non"] * vaccin_num
    )

    probability = 1 / (1 + np.exp(-logit))
    return probability

# Bouton de prédiction
if st.button("Prédire"):
    prob = calculate_probability(eular, anti_ssb, vaccin)
    st.success(f"**Probabilité d'infection :** {prob * 100:.1f}%")

    # Interprétation simple selon seuil de 0.455
    if prob > 0.455:
        st.warning("⚠️ Risque élevé d'infection.")
    else:
        st.info("✅ Risque modéré ou faible d'infection.")

# Documentation
st.markdown("---")
st.markdown("""
**Instructions :**
1. Indiquez les caractéristiques du patient dans la barre latérale.
2. Cliquez sur *Prédire*.
3. La probabilité estimée d'infection et une interprétation s'afficheront ci-dessus.

*Basé sur un modèle de régression logistique validé (AUC = 0.886). these doctorat en medecine generale par ODOI TIMOTHEE PRESTON BRADLEY/+237657691776 *
""")
