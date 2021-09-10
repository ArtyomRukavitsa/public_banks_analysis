import streamlit as st
from classes.diagrams import Diagrams
#from classes.train_model import BinaryClassifierModel
from const_for_main import *
import sqlite3
import folium
from streamlit_folium import folium_static
import pandas as pd
from folium.plugins import FastMarkerCluster

d = Diagrams()
def primary_page():
    st.title("Анализ отзывов клиентов на банковские каналы обслуживания и продукты/услуги")
    st.title('')
    #st.header("Что это за проект?")
    st.subheader("Наш сайт позволяет сравнить любой банк с рынком в среднем и с лучшими "
                "игроками рынка, определить области улучшения и дальнейшего развития "
                "каналов обслуживания, продуктов и услуг по определенным критериям: ")
    st.markdown("<font size='+1'>•	удобство офиса, </font>"
                "<br ><font size='+1'>•	банкоматы, </font>"
                "<br ><font size='+1'>•	касса, </font>"
                "<br ><font size='+1'>•	уровень сервиса, </font>"
                "<br ><font size='+1'>•	персонал, </font>"
                "<br ><font size='+1'>• продукты и услуги, </font>"
                "<br ><font size='+1'>•	дистанционное обслуживание. </font>", unsafe_allow_html=True)
    st.subheader("В качестве входных данных мы используем отзывы с картографического "
                "сервиса Яндекс.Карты (www.yandex.ru/maps) на банковские отделения.")
    st.subheader("")
    st.subheader("На нашем сайте есть следующие страницы:")
    st.subheader("Средняя оценка по всем банкам")#мб добавить URL
    st.markdown("<p align='justify'style='text-indent: 25px;'><font size='+1'>Диаграмма средней оценки по всем банкам строится на основе "
                "оценок всех отзывов на отделения всех банков в выбранных регионах за выбранное время. "
                "Каждая строчка данной диаграммы соответствует определённой категории, также самая "
                "нижняя строчка — это средняя оценка по всем категория. Категории и среднее отличаются "
                "цветами: категории отмечены жёлтым, общее среднее — красным.</font></p>", unsafe_allow_html=True)
    st.subheader("Средние оценки категорий по банкам и регионам")
    st.markdown("<p align='justify'style='text-indent: 25px;'><font size='+1'>Эта диаграмма представлена в формате паутинки. "
                "Шесть лучей, исходящих из одной точки, соответствуют шести категориям. Чем ближе к центру, "
                "тем хуже оценка. И наоборот, чем дальше, тем лучше. Возможен выбор банков, регионов и периода времени, "
                "по которым будет проведён анализ.</font></p>", unsafe_allow_html=True)
    st.markdown("<p align='justify'style='text-indent: 25px;'><font size='+1'>Для предоставления более полного анализа мы решили сделать "
                "диаграммы на основе тех же данных, но показывать не среднюю оценку по категориям, а процентное соотношение "
                "отзывов с положительной и отрицательными оценками по категориям для каждого "
                "выбранного банка. Период времени, выбранный в “паутинке”, также используется при "
                "выборке данных для данной диаграммы. В качестве положительных оценок мы "
                "рассматриваем только 4 и 5, отрицательных — 1 и 2. Отзывы с оценкой 3 не анализируются.</font></p>", unsafe_allow_html=True)
    st.subheader("Важные слова для различных категорий")
    st.markdown("<p align='justify'style='text-indent: 25px;'><font size='+1'>На самой диаграмме представлены отсортированные по "
                "важности десять слов (именно на данных о важности строится график). Важность всех слов в сумме "
                "составляет единицу. Пользователь имеет возможность выбрать из элементов выпадающего списка ту категорию, "
                "которая будет ему интересна.</font></p>", unsafe_allow_html=True)
    st.subheader("Интерактивная карта банковских отделений")
    st.markdown("<p align='justify'style='text-indent: 25px;'><font size='+1'>Пользователю предлагается возможность отобразить конкретные "
                "банки по конкретным регионам, либо сразу же все банки по регионам. При нажатии на конкретный маркер "
                "отображается информация, по которой можно сделать выбор в пользу того и иного отделения</font></p>", unsafe_allow_html=True)
    st.header("")
    st.header("Банки, которые мы анализируем:")
    d   = {' ': ['Сбербанк', 'Банк ВТБ', 'Альфа-Банк', 'Газпромбан', 'Россельхозбанк', 'Почта Банк',
                                           'Банк Открытие', 'Росбанк', 'Совкомбанк', 'Райффайзенбанк', 'Промсвязьбанк', 'Банк Хоум Кредит',
                                           'Банк ДОМ.РФ', 'Уралсиб', 'ЮниКредит', 'Сетелем Банк', 'Русфинанс Банк', 'Ренессанс Кредит',
                                           'Московский кредитный банк', 'Банк Санкт-Петербург', 'СМП Банк',
                                           'МИнБанк', 'УБРиР банк', 'Ситибанк']}
    df = pd.DataFrame(data=d)
    st.dataframe(df, 800, 2400)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Контакты:")
        st.markdown("<font size='+1'>@rukavitsa_a</font><br ><font size='+1'>@fedchenko_a</font>", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)
    with col2:
        st.subheader("Проект выполнен по заказу М.В.Чамрова.")

def diagram_average_for_country():
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


def diagram_average_for_regions_and_banks():
    """
    1) Диаграмма в формате "паутина" для определенных банков и определенных регионов с выбором промежутка времени
    2) Диаграмма в формате "торнадо" для определенных банков и определенных регионов с выбором промежутка времени
    3) Диаграмма в формате "торнадо" с применением критерия согласия Пирсона, к-ый позволяет убрать распределения
        положительных и отрицательных отзывов в банке, схожие с итоговым распределением
    4) Диаграмма в формате "торнадо" с применением критерия согласия Пирсона, к-ый позволяет убрать распределения
        положительных и отрицательных отзывов в банке, схожие с распределениями в категориях с другими банками
    """
    st.title('Средние оценки категорий по банкам и регионам')
    options = st.multiselect(
        'Выберите банки',
        banks,
        ['Среднее по всем банкам']
    )

    region = st.multiselect(
        'Выберите регионы',
        regions,
        ['0 Вся Россия']
    )
    years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    col1, col2 = st.columns(2)
    with col1:
        from_year_ = st.selectbox('Выберите год начала:', years, index=0)
    with col2:
        to_year_ = st.selectbox('Выберите год окончания:', years, index=(len(years) - 1))

    if from_year_ > to_year_:
        st.write('Год начала не может быть меньше года конца')
    else:
        if region and options:
            if len(options) >= 5:
                st.write("Для удобства отображения данных убедительная просьба не выбирать больше четырёх банков")
            else:
                result = d.radarChart(options, region, [from_year_, to_year_])
                if result:
                    result_diagram, has_zero = result
                    # st.write('Средние оценки категорий по банкам и регионам')

                    st.plotly_chart(result_diagram, use_container_width=True)
                    if has_zero:
                        st.write('*Нулевые значения означают отсутствие отзывов по данной категории/оси.*')
                    st.subheader('Диаграмма сравнения процентного соотношения отзывов с положительной и '
                                 'отрицательной оценками для каждого выбранного банка по категориям')
                    st.subheader('*Положительные — оценка 4 или 5*')
                    st.subheader('*Отрицательные — оценка 1 или 2*')
                    if(len(options)>1):
                        version_of_tornado = st.radio('Выберите тип диаграммы "торнадо"', ("Показать все категории", "Показать только те категории, которые "
                        "существенно отличаются от итогового распределения внутри банка", "Показать только те, которые "
                        "сильно отличают выбранные банки"))
                    else:
                        version_of_tornado = st.radio('Выберите тип диаграммы "торнадо"', (
                        "Показать все категории", "Показать только те категории, которые "
                                                  "существенно отличаются от итогового распределения внутри банка"))

                    columns = st.columns(len(options))
                    list_categories = []
                    if(len(options)>1):
                                list_categories = d.tornadoChartBetweenBanks(options, region, [from_year_, to_year_])
                    for i in range(len(columns)):
                        with columns[i]:
                            chart = d.tornadoChartAverage(options[i], region, len(options), [from_year_, to_year_])
                            chart1 = d.tornadoChartInBank(options[i], region, len(options), [from_year_, to_year_])
                            if(len(options)>1):
                                chart2 = d.tornadoChart(options[i], list_categories[i], len(options))
                            if(version_of_tornado == "Показать все категории"):
                                st.plotly_chart(chart)
                            if (version_of_tornado == "Показать только те категории, которые "
                                                  "существенно отличаются от итогового распределения внутри банка"):
                                st.plotly_chart(chart1)
                            if(len(options)>1 and version_of_tornado == "Показать только те, которые сильно отличают "
                                                                        "выбранные банки"):
                                st.plotly_chart(chart2)

                    if has_zero:
                        st.write('*Нулевые значения означают отсутствие отзывов по данной категории/оси.*')
                else:
                    st.write('Одного или нескольких из выбранных банков нет в выбранных регионах.')
        else:
            st.write('Выберите банки и регионы!')


def interactive_map():
    """
    Интерактивная карта отделений.
    """
    from const_for_main import banks
    st.title("Интерактивная карта банковских отделений страны")
    options = st.multiselect(
        'Выберите банки',
        ['Все банки'] + banks[1:],
        ['Все банки']
    )

    region = st.multiselect(
        'Выберите регионы',
        regions,
        ['0 Вся Россия']
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
        with st.spinner("Подождите, пожалуйста"):
            if 'Все банки' in options and len(options) != 1:
                st.write('Выберите "Все банки" либо конкретные банки!')
            elif '0 Вся Россия' in region and len(region) != 1:
                st.write('Выберите "0 Вся Россия" либо конкретные регионы!')
            else:
                for option in options:
                    if option == 'Все банки':
                        selected_id_banks.append(0)
                        break
                    for i in range(len(banks)):
                        if option == banks[i][1]:
                            selected_id_banks.append(i + 1)

                for reg in region:
                    if reg == '0 Вся Россия':
                        selected_id_regions.append(0)
                        location = [63.391425, 59.844655]
                        zoom_start = 4
                        break
                    else:
                        selected_id_regions.append(int(reg.split()[0]))
                has_markers = False
                con = sqlite3.connect(CONNECTION)
                cur = con.cursor()
                for address in addresses:
                    if (address[2] in selected_id_banks or selected_id_banks[0] == 0) and \
                            (selected_id_regions[0] == 0 or address[3] in selected_id_regions) and not (address[7] is None):
                        bankName = banks[int(address[2]) - 1][1]
                        add = address[1]
                        if address[7] != 0:
                            avg_rate = f"Средняя оценка: {address[7]}"
                            other_marks = list(cur.execute("SELECT "
                                                           "avg_c1, avg_c2, avg_c3, avg_c4, avg_c5, avg_c6,"
                                                           "per_c1, per_c2, per_c3, per_c4, per_c5, per_c6,"
                                                           "count "
                                                           "FROM addresses "
                                                           "WHERE id=?", [address[0]]).fetchone())
                            avg_rate += f"<br>Количество отзывов: {other_marks[12]}"
                            for i in range(6):
                                if other_marks[i] == 0:
                                    other_marks[i] = "нет отзывов"
                            for i in range(6):
                                if other_marks[6 + i] == 0:
                                    other_marks[6 + i] = "0"
                            avg_rate += f"<br><br>Оценки по категориям:<br>" \
                                        f"<table width='100%' border='1'>" \
                                        f"<tr>" \
                                        f"<th> Категория </th>" \
                                        f"<th> Средняя оценка </th>" \
                                        f"<th> % отзывов </th>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> Удобство офиса </td>" \
                                        f"<td> {other_marks[0]} </td>" \
                                        f"<td> {other_marks[6]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> Банкоматы </td>" \
                                        f"<td> {other_marks[1]} </td>" \
                                        f"<td> {other_marks[7]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> Уровень сервиса </td>" \
                                        f"<td> {other_marks[2]} </td>" \
                                        f"<td> {other_marks[8]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> Персонал </td>" \
                                        f"<td> {other_marks[3]} </td>" \
                                        f"<td> {other_marks[9]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> Продукты и услуги </td>" \
                                        f"<td> {other_marks[4]} </td>" \
                                        f"<td> {other_marks[10]}% </td>" \
                                        f"</tr>" \
                                        f"<tr>" \
                                        f"<td> Дист. каналы обслуживания </td>" \
                                        f"<td> {other_marks[5]} </td>" \
                                        f"<td> {other_marks[11]}% </td>" \
                                        f"</tr>" \
                                        f"</table>" \

                            print(other_marks)
                        else:
                            avg_rate = "<b>Оценок нет.<b>"
                        string = f"{bankName}, {add}.<br>{avg_rate}"
                        arr.append([
                            float(address[4]),
                            float(address[5]),
                            links[int(address[2])],
                            string
                        ])
                        if not location:
                            location = [float(address[4]), float(address[5])]
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


def important_words():
    """
    Диаграмма "Важные слова по категориям"
    """
    st.title("Важные слова для различных категорий")
    choices = categories[1:]
    category = st.selectbox('Выберите категорию:', choices, index=0)
    i = choices.index(category)
    d = Diagrams()
    st.plotly_chart(d.important_words_and_coefs(important_words_for_each_category[i][0], \
                                                important_words_for_each_category[i][1]), use_container_width=True)

