import streamlit as st
from utils.display_results import *

def main():
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose",
        ["Home", "Predictions", "Postprocessing"])
    if app_mode == "Home":
        st.subheader("👁️ Présentation de l'endothélium cornéen")
        st.markdown("""
        L'endothélium cornéen est une couche cellulaire essentielle à la transparence de la cornée.
        Cette application vous permet :
        - de charger une image issue d'une segmentation
        - de calculer les propriétés cellulaires (aire, circularité, densité...)
        - de détecter les cellules hexagonales
        - d'exporter les résultats
        """)
    elif app_mode == "Postprocessing":
        st.subheader("Image analysis")
        postprocessing_view()
    
          
    else:
        st.info("Working in progress")

if __name__ == "__main__":
    main()