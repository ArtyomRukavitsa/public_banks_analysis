import streamlit as st
from diagrams_functions import *
from const_for_main import LANGUAGES


st.set_page_config(layout="wide")
language = ['Русский', "English"]
selected_language = st.sidebar.radio("Выберите язык / Select language:", language)
number_of_language = 0 if selected_language == "Русский" else 1

pages = {LANGUAGES['menu'][0][number_of_language]: primary_page,
         LANGUAGES['menu'][1][number_of_language]: diagram_average_for_country,
         LANGUAGES['menu'][2][number_of_language]: diagram_average_for_regions_and_banks,
         LANGUAGES['menu'][3][number_of_language]: important_words,
         LANGUAGES['menu'][4][number_of_language]: interactive_map
         }

st.sidebar.title(LANGUAGES['menu'][5][number_of_language])
choice = st.sidebar.radio(LANGUAGES['menu'][6][number_of_language], tuple(pages.keys()))
pages[choice](number_of_language)
