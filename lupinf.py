import streamlit as st
import numpy as np

# Titre de l'application
st.title("Prédiction du Risque Infectieux chez les Patients Lupiques 🔍")

# Sidebar pour les inputs utilisateur
with st.sidebar:
    st.header("Paramètres du Patient")
    eular = st.number_input("Score EULAR_ACR_2019", min_value=0, max_value=100, value=10)
    anti_ssb = st.selectbox("Anti-SSB", ["Positif", "Négatif"])
    vaccin = st.selectbox("Vaccin Pneumocoque", ["Non", "Oui"])

# Coefficients du modèle (extraits de R)
COEFFICIENTS = {
    "intercept": -3.64773,
    "eular": 0.14567,
    "anti_ssb_positif": 2.13716,
    "vaccin_non": 3.85932
}


# Calcul de la prédiction
def calculate_probability(eular, anti_ssb, vaccin):
    # Conversion des inputs en valeurs numériques
    anti_ssb_num = 1 if anti_ssb == "Positif" else 0
    vaccin_num = 1 if vaccin == "Non" else 0

    # Équation logit
    logit = (
            COEFFICIENTS["intercept"]
            + COEFFICIENTS["eular"] * eular
            + COEFFICIENTS["anti_ssb_positif"] * anti_ssb_num
            + COEFFICIENTS["vaccin_non"] * vaccin_num
    )

    # Conversion en probabilité
    probability = 1 / (1 + np.exp(-logit))
    return probability


# Bouton de prédiction
if st.button("Prédire"):
    prob = calculate_probability(eular, anti_ssb, vaccin)
    st.success(f"**Probabilité d'infection :** {prob * 100:.1f}%")

    # Interprétation
    if prob > 0.7:
        st.warning("Risque élevé : des mesures préventives sont recommandées.")
    else:
        st.info("Risque modéré ou faible.")

# Documentation
st.markdown("---")
st.markdown("""
**Comment utiliser :**
1. Ajustez les paramètres dans la barre latérale.
2. Cliquez sur *Prédire*.
3. Consultez l'interprétation ci-dessus.
""")