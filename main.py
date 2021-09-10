import streamlit as st
from diagrams_functions import *


st.set_page_config(layout="wide")
pages = {'Главная': primary_page,
         'Средняя оценка по всем банкам': diagram_average_for_country,
         'Средние оценки категорий по банкам и регионам': diagram_average_for_regions_and_banks,
         'Важные слова для различных категорий': important_words,
         'Интерактивная карта банковских отделений': interactive_map
         }

st.sidebar.title('Меню')
choice = st.sidebar.radio("Выберите страницу:", tuple(pages.keys()))
pages[choice]()
