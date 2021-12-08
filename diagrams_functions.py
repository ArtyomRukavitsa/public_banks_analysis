import streamlit as st
from classes.diagrams import Diagrams
#from classes.train_model import BinaryClassifierModel
from const_for_main import *
import sqlite3
import folium
from streamlit_folium import folium_static
import pandas as pd
from folium.plugins import FastMarkerCluster
import streamlit.components.v1 as components
d = Diagrams()


def primary_page(number_of_language):
    st.title(LANGUAGES["primary_page"][0][number_of_language])
    st.title('')
    #st.header("Что это за проект?")
    st.subheader(LANGUAGES["primary_page"][1][number_of_language])
    st.markdown(f"<font size='+1'>•	{LANGUAGES['primary_page'][2][number_of_language]}, </font>"
                f"<br ><font size='+1'>• {LANGUAGES['primary_page'][3][number_of_language]}, </font>"
                f"<br ><font size='+1'>• {LANGUAGES['primary_page'][4][number_of_language]}, </font>"
                f"<br ><font size='+1'>• {LANGUAGES['primary_page'][5][number_of_language]}, </font>"
                f"<br ><font size='+1'>• {LANGUAGES['primary_page'][6][number_of_language]}, </font>"
                f"<br ><font size='+1'>• {LANGUAGES['primary_page'][7][number_of_language]} </font>", unsafe_allow_html=True)
    st.subheader(LANGUAGES['primary_page'][8][number_of_language])
    st.subheader("")
    st.subheader(LANGUAGES['primary_page'][9][number_of_language])
    with st.expander(LANGUAGES['primary_page'][10][number_of_language]):
        st.markdown(
            f"<p align='justify'style='text-indent: 25px;'><font size='+1'>"
            f"{LANGUAGES['primary_page'][11][number_of_language]}"
            f"</font></p>", unsafe_allow_html=True)

    with st.expander(LANGUAGES['primary_page'][12][number_of_language]):
        st.markdown(
            f"<p align='justify'style='text-indent: 25px;'><font size='+1'>"
            f"{LANGUAGES['primary_page'][13][number_of_language]}"
            f"</font></p>", unsafe_allow_html=True)
        st.markdown(
            f"<p align='justify'style='text-indent: 25px;'><font size='+1'>"
            f"{LANGUAGES['primary_page'][14][number_of_language]}"
            f"</font></p>",
            unsafe_allow_html=True)
    with st.expander(LANGUAGES['primary_page'][15][number_of_language]):
        st.markdown(
            f"<p align='justify'style='text-indent: 25px;'>"
            f"{LANGUAGES['primary_page'][16][number_of_language]}"
            f"<font size='+1'></font></p>", unsafe_allow_html=True)
    with st.expander(LANGUAGES['primary_page'][17][number_of_language]):
        st.markdown(
            f"<p align='justify'style='text-indent: 25px;'>"
            f"{LANGUAGES['primary_page'][18][number_of_language]}"
            f"<font size='+1'></font></p>",
            unsafe_allow_html=True)
    st.header("")
    st.header(LANGUAGES['primary_page'][19][number_of_language])
    d = {' ': LANGUAGES['primary_page'][20][number_of_language]}
    df = pd.DataFrame(data=d)
    st.dataframe(df, 800, 2400)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(LANGUAGES['primary_page'][21][number_of_language])
        st.markdown("<font size='+1'>@rukavitsa_a</font><br ><font size='+1'>@fedchenko_a</font>", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)
    with col2:
        st.subheader(LANGUAGES['primary_page'][22][number_of_language])

    components.html(
        f"""
                <script>
                    window.parent.document.querySelector('section.main').scrollTo(0, 0);
                </script>
            """,
        height=0
    )

def diagram_average_for_country(number_of_language):
    """
    Построение диаграммы средних оценок для всех банков и всех регионов с выбором промежутка времени.
    """
    st.title("Средняя оценка по всем банкам")
    years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    col1, col2 = st.columns(2)
    with col1:
        from_year = st.selectbox('Выберите год начала:', years, index=0)
    with col2:
        to_year = st.selectbox('Выберите год окончания:', years, index=(len(years) - 1))

    if from_year > to_year:
        st.write('Год начала не может быть меньше года конца')
    else:
        #print(from_years, to_years)
        st.plotly_chart(d.horizontalChartAverage([from_year, to_year]), use_container_width=True)


def diagram_average_for_regions_and_banks(number_of_language):
    """
    1) Диаграмма в формате "паутина" для определенных банков и определенных регионов с выбором промежутка времени
    2) Диаграмма в формате "торнадо" для определенных банков и определенных регионов с выбором промежутка времени
    3) Диаграмма в формате "торнадо" с применением критерия согласия Пирсона, к-ый позволяет убрать распределения
        положительных и отрицательных отзывов в банке, схожие с итоговым распределением
    4) Диаграмма в формате "торнадо" с применением критерия согласия Пирсона, к-ый позволяет убрать распределения
        положительных и отрицательных отзывов в банке, схожие с распределениями в категориях с другими банками
    """
    st.title(LANGUAGES['average_rating'][0][number_of_language])

    array_banks = banks[1:] if number_of_language == 0 else banks_en

    options = st.multiselect(
        LANGUAGES['average_rating'][1][number_of_language],
        [LANGUAGES["average_rating"][2][number_of_language]] + array_banks,
        [LANGUAGES["average_rating"][2][number_of_language]]
    )

    if number_of_language == 0:
        region = st.multiselect(
            LANGUAGES["average_rating"][3][number_of_language],
            regions,
            ['0 Вся Россия']
        )
    else:
        region = st.multiselect(
            LANGUAGES["average_rating"][3][number_of_language],
            regions_en,
            ['0 Russia']
        )

    years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    col1, col2 = st.columns(2)
    with col1:
        from_year_ = st.selectbox(LANGUAGES["average_rating"][5][number_of_language], years, index=0)
    with col2:
        to_year_ = st.selectbox(LANGUAGES["average_rating"][6][number_of_language], years, index=(len(years) - 1))

    if from_year_ > to_year_:
        st.write('Год начала не может быть меньше года конца')
    else:
        if region and options:
            if len(options) >= 5:
                st.write("Для удобства отображения данных убедительная просьба не выбирать больше четырёх банков")
            else:
                selected_regions = []
                selected_banks = []
                if number_of_language == 1:
                    if options[0] == "All banks":
                        selected_banks = ["Среднее по всем банкам"]
                    if len(options) > 1:
                        for elem in options:
                            if elem != "All banks":
                                selected_banks.append(banks[banks_en.index(elem) + 1])

                    if region[0] == "0 Russia":
                        selected_regions = ["0 Вся Россия"]
                    else:
                        for elem in region:
                            selected_regions.append(regions[regions_en.index(elem) + 1])

                else:
                    selected_banks = options.copy()
                    selected_regions = region.copy()

                #print(selected_banks, selected_regions)
                result = d.radarChart(selected_banks, selected_regions, [from_year_, to_year_], number_of_language)
                if result:
                    result_diagram, has_zero = result
                    # st.write('Средние оценки категорий по банкам и регионам')

                    st.plotly_chart(result_diagram, use_container_width=True)
                    if has_zero:
                        st.write('*Нулевые значения означают отсутствие отзывов по данной категории/оси.*')
                    st.subheader('Диаграмма сравнения процентного соотношения отзывов с положительной и '
                                 'отрицательной оценками для каждого выбранного банка по категориям')
                    st.subheader(LANGUAGES["average_rating"][13][number_of_language])
                    st.subheader(LANGUAGES["average_rating"][14][number_of_language])
                    if(len(options)>1):
                        version_of_tornado = st.radio(LANGUAGES["average_rating"][15][number_of_language],
                                                      LANGUAGES["average_rating"][16][number_of_language])
                    else:
                        version_of_tornado = st.radio(LANGUAGES["average_rating"][15][number_of_language],
                                                      LANGUAGES["average_rating"][17][number_of_language])

                    columns = st.columns(len(selected_banks))
                    print(selected_banks)
                    list_categories = []
                    if(len(selected_banks)>1):
                                # list_categories = d.tornadoChartBetweenBanks(options, region, [from_year_, to_year_])
                                list_categories = d.tornadoChartBetweenBanks(selected_banks, selected_regions, [from_year_, to_year_], number_of_language)
                    for i in range(len(columns)):
                        with columns[i]:
                            #chart = d.tornadoChartAverage(options[i], region, len(options), [from_year_, to_year_])
                            #chart1 = d.tornadoChartInBank(options[i], region, len(options), [from_year_, to_year_])
                            chart = d.tornadoChartAverage(selected_banks[i], selected_regions, len(selected_banks), [from_year_, to_year_], number_of_language)
                            chart1 = d.tornadoChartInBank(selected_banks[i], selected_regions, len(selected_banks), [from_year_, to_year_], number_of_language)
                            if(len(selected_banks)>1):
                                print("AAAAAAAAAA")
                                print(options)
                                chart2 = d.tornadoChart(selected_banks[i], list_categories[i], len(selected_banks), number_of_language)
                            if(version_of_tornado == LANGUAGES["average_rating"][16][number_of_language][0]):
                                st.plotly_chart(chart)
                            if (version_of_tornado == LANGUAGES["average_rating"][16][number_of_language][1]):
                                st.plotly_chart(chart1)
                            if(len(options)>1 and version_of_tornado == LANGUAGES["average_rating"][16][number_of_language][2]):
                                st.plotly_chart(chart2)

                    if has_zero:
                        st.write('*Нулевые значения означают отсутствие отзывов по данной категории/оси.*')
                else:
                    st.write('Одного или нескольких из выбранных банков нет в выбранных регионах.')
        else:
            st.write('Выберите банки и регионы!')


def interactive_map(number_of_language):
    """
    Интерактивная карта отделений.
    """
    from const_for_main import banks, banks_en
    st.title(LANGUAGES["interactive_map"][0][number_of_language])

    array_banks = banks[1:] if number_of_language == 0 else banks_en

    options = st.multiselect(
        LANGUAGES["interactive_map"][1][number_of_language],
        [LANGUAGES["interactive_map"][2][number_of_language]] + array_banks,
        [LANGUAGES["interactive_map"][2][number_of_language]]
    )
    print(LANGUAGES["interactive_map"][4][number_of_language])

    if number_of_language == 0:
        region = st.multiselect(
            LANGUAGES["interactive_map"][3][number_of_language],
            regions,
            ['0 Вся Россия']
        )
    else:
        region = st.multiselect(
            LANGUAGES["interactive_map"][3][number_of_language],
            regions_en,
            ['0 Russia']
        )

    callback = ("function (row) {"
                "var icon = L.icon({iconUrl: row[2], iconSize: [24, 24], iconAnchor: [16, 37], popupAnchor: [0, -28]});"
                "var marker = L.marker([row[0], row[1]], {icon: icon}); "
                "var popup = L.popup({maxWidth: '400'});"
                "const display_text = {text: row[3]};"
                "var mytext = $(`<div id='mytext' class='display_text' "
                "style='width: 100.0%; height: 100.0%;'> ${display_text.text}</div>`)[0];"
                "popup.setContent(mytext);"
                "marker.bindPopup(popup);"
                "return marker};")

    arr = []

    con = sqlite3.connect(CONNECTION)
    cur = con.cursor()
    addresses = cur.execute('SELECT * FROM addresses').fetchall()
    banks = cur.execute('SELECT * FROM id_banks').fetchall()
    cur.close()
    con.close()

    selected_id_banks, selected_id_regions = [], []
    location = []
    zoom_start = 0
    if len(options) == 0 or len(region) == 0:
        st.write('Выберите регионы и банки!')

    else:
        with st.spinner(LANGUAGES["interactive_map"][16][number_of_language]):
            if (LANGUAGES["interactive_map"][2][number_of_language] in options) and len(options) != 1:
                st.write('Выберите "Все банки" либо конкретные банки!')
            elif ('0 Вся Россия' in region or '0 Russia' in options) and len(region) != 1:
                st.write('Выберите "0 Вся Россия" либо конкретные регионы!')
            else:
                for option in options:
                    if option == LANGUAGES["interactive_map"][2][number_of_language]:
                        selected_id_banks.append(0)
                        break
                    for i in range(len(banks)):
                        if option == banks[i][1] or option == banks[i][2]:
                            selected_id_banks.append(i + 1)

                for reg in region:
                    if reg in [regions[0], regions_en[0]]:
                        selected_id_regions.append(0)
                        location = [63.391425, 59.844655]
                        zoom_start = 4
                        break
                    else:
                        selected_id_regions.append(int(reg.split()[0]))
                has_markers = False
                con = sqlite3.connect(CONNECTION)
                cur = con.cursor()
                print(selected_id_banks)
                for address in addresses:
                    address_rus = address[1]
                    address_eng = address[2]
                    id_bank = address[3]
                    id_region = address[4]
                    latitude = address[5]
                    longitude = address[6]
                    if (id_bank in selected_id_banks or selected_id_banks[0] == 0) and \
                            (selected_id_regions[0] == 0 or id_region in selected_id_regions) and not (address[-1] is None):
                        if number_of_language == 0:
                            bankName = banks[id_bank - 1][1]
                            add = address_rus
                        else:
                            bankName = banks[id_bank - 1][2]
                            add = address_eng
                        if address[-1] != 0:
                            avg_rate = f"{LANGUAGES['interactive_map'][5][number_of_language]}: {address[7]}"
                            other_marks = list(cur.execute("SELECT "
                                                           "avg_c1, avg_c2, avg_c3, avg_c4, avg_c5, avg_c6,"
                                                           "per_c1, per_c2, per_c3, per_c4, per_c5, per_c6,"
                                                           "count "
                                                           "FROM addresses "
                                                           "WHERE id=?", [address[0]]).fetchone())
                            avg_rate += f"<br>{LANGUAGES['interactive_map'][6][number_of_language]}: {other_marks[12]}"
                            for i in range(6):
                                if other_marks[i] == 0:
                                    other_marks[i] = LANGUAGES['interactive_map'][17][number_of_language]
                            for i in range(6):
                                if other_marks[6 + i] == 0:
                                    other_marks[6 + i] = "0"
                            avg_rate += f"<br><br>{LANGUAGES['interactive_map'][7][number_of_language]}:<br>" \
                                        f"<table width='100%' border='1'>" \
                                        f"<tr>" \
                                        f"<th> {LANGUAGES['interactive_map'][14][number_of_language]} </th>" \
                                        f"<th> {LANGUAGES['interactive_map'][5][number_of_language]} </th>" \
                                        f"<th> {LANGUAGES['interactive_map'][15][number_of_language]} </th>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> {LANGUAGES['interactive_map'][8][number_of_language]} </td>" \
                                        f"<td> {other_marks[0]} </td>" \
                                        f"<td> {other_marks[6]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> {LANGUAGES['interactive_map'][9][number_of_language]} </td>" \
                                        f"<td> {other_marks[1]} </td>" \
                                        f"<td> {other_marks[7]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> {LANGUAGES['interactive_map'][10][number_of_language]} </td>" \
                                        f"<td> {other_marks[2]} </td>" \
                                        f"<td> {other_marks[8]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> {LANGUAGES['interactive_map'][11][number_of_language]} </td>" \
                                        f"<td> {other_marks[3]} </td>" \
                                        f"<td> {other_marks[9]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> {LANGUAGES['interactive_map'][12][number_of_language]} </td>" \
                                        f"<td> {other_marks[4]} </td>" \
                                        f"<td> {other_marks[10]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> {LANGUAGES['interactive_map'][13][number_of_language]} </td>" \
                                        f"<td> {other_marks[5]} </td>" \
                                        f"<td> {other_marks[11]}% </td>" \
                                        f"</tr>" \
                                        f"</table>" \

                            #print(other_marks)
                        else:
                            avg_rate = "<b>Оценок нет.<b>"
                        string = f"{bankName}, {add}.<br>{avg_rate}"
                        arr.append([
                            latitude,
                            longitude,
                            links[id_bank],
                            string
                        ])
                        if not location:
                            location = [latitude, longitude]
                            zoom_start = 5
                        has_markers = True
                if has_markers:
                    m = folium.Map(location=location, zoom_start=zoom_start)
                    df = pd.DataFrame(arr, columns=['lat', 'lon', 'link', 'string'])
                    m.add_child(
                        FastMarkerCluster(df[['lat', 'lon', 'link', 'string']].values.tolist(), callback=callback))
                    container = st.container()

                    with container:
                        folium_static(m, width=1350)
                else:
                    st.write('Выбранных банков нет в выбранных регионах!')
                cur.close()
                con.close()


def important_words(number_of_language):
    """
    Диаграмма "Важные слова по категориям"
    """
    st.title(LANGUAGES['imp_words'][0][number_of_language])
    choices = categories[1:] if number_of_language == 0 else categories_en[1:]
    imp = important_words_for_each_category if number_of_language == 0 else important_words_for_each_category_en
    category = st.selectbox(LANGUAGES['imp_words'][1][number_of_language], choices, index=0)
    i = choices.index(category)
    d = Diagrams()
    st.plotly_chart(d.important_words_and_coefs(imp[i][0], imp[i][1]), use_container_width=True)

