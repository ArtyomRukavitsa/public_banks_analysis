from pprint import pprint

import plotly.express as px
import sqlite3
import plotly.graph_objects as go
from scipy.stats import chi2_contingency

from const_for_main import *
import chart_studio


class Diagrams:
    """
    Класс для работы с диаграммами (построение, поиск нужных данных)
    """
    def __init__(self):
        pass

    def getAverageRateForCountry(self, region: list, years: list):
        """
        Получение средних оценок по всем категориям и по отдельности для всех банков из БД.
        region : list -- список регионов, по которым строится анализ.
        years: list -- период, за который нужно производить визуализацию

        return:
        [averageAll, averageConvenience, averageAtm, averageService_level,
        averageStaff, averageProducts_services, averageRemote_service]

        averageAll : float -- средняя оценка по всем категориям
        averageConvenience : float -- средняя оценка по категории "Удобство банка"
        averageAtm : float -- средняя оценка по категории "Банкоматы"
        averageService_level : float -- средняя оценка по категории "Уровень сервиса"
        averageStaff : float -- средняя оценка по категории "Персонал"
        averageProducts_services : float -- средняя оценка по категории "Продукты и услуги"
        averageRemote_service : float -- средняя оценка по категории "Дистанционные каналы обслуживания"
        """
        con = sqlite3.connect(CONNECTION)
        from_year, to_year = years
        cur = con.cursor()
        if region[0] == '0 Вся Россия':
            string = ""
        else:
            string = " AND "
            for reg in region:
                string += f"id_region={int(reg.split()[0])} OR "
            string = string[:-4]
            # string += ")"
        if string:
            string2 = "WHERE" + string[4:]
            string2 += f" AND year >= {from_year} AND year <= {to_year}"
        else:
            string2 = f" WHERE year >= {from_year} AND year <= {to_year}"

        string += f" AND year >= {from_year} AND year <= {to_year}"
        print(string2)
        # print(string)
        print("SELECT rate FROM reviews " + string2)
        if region[0] == '0 Вся Россия':
            all_reviews = cur.execute("SELECT rate FROM reviews" + string2).fetchall()
            averageAll = sum([x[0] for x in all_reviews]) / len(all_reviews)
        else:
            averageAll = 0

        convenience = cur.execute("SELECT rate FROM reviews WHERE c1=1" + string).fetchall()
        if len(convenience) == 0:
            averageConvenience = 0
        else:
            averageConvenience = sum([x[0] for x in convenience]) / len(convenience)


        atm = cur.execute("SELECT rate FROM reviews WHERE c2=1" + string).fetchall()
        if len(atm) == 0:
            averageAtm = 0
        else:
            averageAtm = sum([x[0] for x in atm]) / len(atm)

        service_level = cur.execute("SELECT rate FROM reviews WHERE c3=1" + string).fetchall()
        if len(service_level) == 0:
            averageService_level = 0
        else:
            averageService_level = sum([x[0] for x in service_level]) / len(service_level)

        staff = cur.execute("SELECT rate FROM reviews WHERE c4=1" + string).fetchall()
        if len(staff) == 0:
            averageStaff = 0
        else:
            averageStaff = sum([x[0] for x in staff]) / len(staff)

        products_services = cur.execute("SELECT rate FROM reviews WHERE c5=1" + string).fetchall()
        if len(products_services) == 0:
            averageProducts_services = 0
        else:
            averageProducts_services = sum([x[0] for x in products_services]) / len(products_services)

        remote_service = cur.execute("SELECT rate FROM reviews WHERE c6=1" + string).fetchall()
        if len(remote_service) == 0:
            averageRemote_service = 0
        else:
            averageRemote_service = sum([x[0] for x in remote_service]) / len(remote_service)

        cur.close()
        con.close()
        return [averageAll,
                averageConvenience, averageAtm,
                averageService_level, averageStaff, averageProducts_services, averageRemote_service]

    def horizontalChartAverage(self, years: list, number_of_language: int):
        """
        Построение горизонтальной гистаграммы, которая визуализирует средние оценки по
        категориям и среднюю оценку всех отзывов для всех отделений банков РФ.
        years: list -- период, за который нужно производить визуализацию

        return:
        fig : plotly.graph_objects.Figure -- построенная диаграмма.
        """
        categories_in_chart = categories if number_of_language == 0 else categories_en
        averageAll, \
        averageConvenience, \
        averageAtm, \
        averageService_level, \
        averageStaff, \
        averageProducts_services, \
        averageRemote_service = self.getAverageRateForCountry(['0 Вся Россия'], years)
        fig = px.bar(x=[
            averageAll,
            averageConvenience,
            averageAtm,
            averageService_level,
            averageStaff,
            averageProducts_services,
            averageRemote_service
        ],
            y=categories_in_chart,
            labels={
                'x': 'rate',
                'y': 'categories'},
            color=["red", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"],
            color_discrete_map="identity",
            height=500,
            # title="Средняя оценка по всем банкам",
            text=[
                round(averageAll, 2),
                round(averageConvenience, 2),
                round(averageAtm, 2),
                round(averageService_level, 2),
                round(averageStaff, 2),
                round(averageProducts_services, 2),
                round(averageRemote_service, 2)
            ])
        return fig

    def getAverageRateForBank(self, id_bank: int, region: list, years: list):
        """
        Получение средних оценок по категориям для определенного банка в определенных регионах.
        id_bank : int -- идентификатор банка в БД
        region : list -- список идентификаторов регионов, для которых необходимо построить диаграмму.
        years: list -- период, за который нужно производить визуализацию

        return:
        [averageConvenience, averageAtm, averageService_level,
        averageStaff, averageProducts_services, averageRemote_service]

        averageConvenience : float -- средняя оценка по категории "Удобство банка"
        averageAtm : float -- средняя оценка по категории "Банкоматы"
        averageService_level : float -- средняя оценка по категории "Уровень сервиса"
        averageStaff : float -- средняя оценка по категории "Персонал"
        averageProducts_services : float -- средняя оценка по категории "Продукты и услуги"
        averageRemote_service : float -- средняя оценка по категории "Дистанционные каналы обслуживания"

        """
        from_year, to_year = years
        con = sqlite3.connect(CONNECTION)
        cur = con.cursor()
        if region[0] == '0 Вся Россия':
            string = ""
        else:
            string = "AND id_region IN ("
            for reg in region:
                string += f"{str(reg.split()[0])}, "
            string = string[:-2]
            string += ")"
        string2 = f" AND year >= {from_year} AND year <= {to_year}"
        all_reviews = cur.execute("SELECT rate FROM reviews WHERE id_bank=?" + string + string2, (id_bank,)).fetchall()
        if not all_reviews:
            return None
        # averageAll = sum([x[0] for x in all_reviews]) / len(all_reviews)

        convenience = cur.execute("SELECT rate FROM reviews WHERE c1=1 AND id_bank=?" + string + string2, (id_bank,)).fetchall()
        if len(convenience) == 0:
            averageConvenience = 0
        else:
            averageConvenience = sum([x[0] for x in convenience]) / len(convenience)

        atm = cur.execute("SELECT rate FROM reviews WHERE c2=1 AND id_bank=?" + string + string2, (id_bank,)).fetchall()
        if len(atm) == 0:
            averageAtm = 0
        else:
            averageAtm = sum([x[0] for x in atm]) / len(atm)

        service_level = cur.execute("SELECT rate FROM reviews WHERE c3=1 AND id_bank=?" + string + string2, (id_bank,)).fetchall()
        if len(service_level) == 0:
            averageService_level = 0
        else:
            averageService_level = sum([x[0] for x in service_level]) / len(service_level)

        staff = cur.execute("SELECT rate FROM reviews WHERE c4=1 AND id_bank=?" + string + string2, (id_bank,)).fetchall()
        if len(staff) == 0:
            averageStaff = 0
        else:
            averageStaff = sum([x[0] for x in staff]) / len(staff)

        products_services = cur.execute("SELECT rate FROM reviews WHERE c5=1 AND id_bank=?" + string + string2,
                                        (id_bank,)).fetchall()
        if len(products_services) == 0:
            averageProducts_services = 0
        else:
            averageProducts_services = sum([x[0] for x in products_services]) / len(products_services)

        remote_service = cur.execute("SELECT rate FROM reviews WHERE c6=1 AND id_bank=?" + string + string2,
                                     (id_bank,)).fetchall()
        if len(remote_service) == 0:
            averageRemote_service = 0
        else:
            averageRemote_service = sum([x[0] for x in remote_service]) / len(remote_service)

        cur.close()
        con.close()
        return [averageConvenience, averageAtm, averageService_level,
                averageStaff, averageProducts_services, averageRemote_service]

    def radarChart(self, selected_banks: list, selected_regions: list, years: list, number_of_language: int):
        """
        Построение диаграммы в формате "паутина", которая позволяет сравнить различные банки по всем категориям
        selected_banks: list -- идентификаторы выбранных пользователем банков
        selected_regions: list -- идентификаторы выбранных пользователем регионов
        years: list -- период, за который нужно производить визуализацию
        number_of_language: int -- индентификатор языка интерфеса
        return:
        [fig, has_zero]

        fig : plotly.graph_objects.Figure -- построенная диаграмма
        has_zero : bool -- флаг, который указывает, есть ли нулевые показатели в диаграмме (т.е. на нее нет отзывов).
                            True -- есть хотя бы одна категория без отзывов
                            False -- на все категории есть отзывы
                            Данный флаг нужен для отображения информации для пользователя о наличии нулевых категорий.
        """
        categories_in_chart = categories if number_of_language == 0 else categories_en
        fig = go.Figure()
        is_in_region = True
        has_zero = False

        for elem in selected_banks:
            if elem == 'Среднее по всем банкам' or elem == "All banks":
                averageAll, \
                averageConvenience, \
                averageAtm, \
                averageService_level, \
                averageStaff, \
                averageProducts_services, \
                averageRemote_service = self.getAverageRateForCountry(selected_regions, years)
            else:
                id_bank = banks.index(elem)
                result = self.getAverageRateForBank(id_bank, selected_regions, years)
                if not result:  # прилетел из метода None
                    is_in_region = False
                    break
                else:
                    averageConvenience, \
                    averageAtm, \
                    averageService_level, \
                    averageStaff, \
                    averageProducts_services, \
                    averageRemote_service = result
                    if any(elem == 0 for elem in result):
                        has_zero = True

            if is_in_region:
                if number_of_language == 1:
                    if elem != "Среднее по всем банкам":
                        elem = banks_en[banks.index(elem) - 1]
                    else:
                        elem = "All banks"
                avg_rate = round((averageConvenience + averageAtm + averageService_level +
                                  averageStaff + averageProducts_services + averageRemote_service) / 6, 2)
                fig.add_trace(go.Scatterpolar(
                    r=[
                        averageConvenience,
                        averageAtm,
                        averageService_level,
                        averageStaff,
                        averageProducts_services,
                        averageRemote_service,
                        averageConvenience
                    ],
                    theta=categories_in_chart[1:] + [categories_in_chart[1]],
                    # fill='toself',
                    name=elem + f" ({avg_rate})",
                    # fillcolor=colours[elem][0],
                    marker=dict(color=colours[elem][0]),
                    opacity=0.6,

                ))
        if is_in_region:
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5],
                    )),
                showlegend=True,
                height=600
                # title='Средние оценки категорий по банкам и регионам'
            )

        if not is_in_region:
            return None
        return [fig, has_zero]

    def getPositiveAndNegativeShareForCategories(self, bankName: str, region: list, flag: bool, years: list):
        """
        Получение доли позитивных (оценки 4 и 5) и негативных (оценки 1 и 2)
        отзывов на определенный банк по выбранным регионам

        bankName: str -- название банка
        region: list -- список выбранных пользователем регионов
        flag : bool -- флаг для возвращения тех или иных значений
        years: list -- период, за который нужно производить визуализацию

        return:
        if bool:
        [
            [(conveniencePositive * 100) // convenience, (convenienceNegative * 100) // convenience],
            [(atmPositive * 100) // atm, (atmNegative * 100) // atm],
            [(servicePositive * 100) // service, (serviceNegative * 100) // service],
            [(staffPositive * 100) // staff, (staffNegative * 100) // staff],
            [(productsPositive * 100) // products, (productsNegative * 100) // products],
            [(remotePositive * 100) // remote, (remoteNegative * 100) // remote],
        ]

        Каждый список двумерного списка содержит два числа типа float,
        обозначающие позитивные и негативные доли соответственно.
        Вложенные списки содержат информацию по категориям по следующему порядку:
                "Удобство офиса", "Банкоматы", "Уровень сервиса",
                "Персонал", "Продукты и услуги", "Дистанционные каналы обслуживания"

        if not bool:
        [
                [conveniencePositive, convenienceNegative, (conveniencePositive * 100) // convenience, (convenienceNegative * 100) // convenience],
                [atmPositive, atmNegative, (atmPositive * 100) // atm, (atmNegative * 100) // atm],
                [servicePositive, serviceNegative, (servicePositive * 100) // service, (serviceNegative * 100) // service],
                [staffPositive, staffNegative, (staffPositive * 100) // staff, (staffNegative * 100) // staff],
                [productsPositive, productsNegative, (productsPositive * 100) // products, (productsNegative * 100) // products],
                [remotePositive, remoteNegative, (remotePositive * 100) // remote, (remoteNegative * 100) // remote],
                [resultPositive/result, resultNegative/result],
            ]
        В каждом подсписке содержатся кол-во положительных и отрицательных отзывов, а также их доли.
        Последний подписок -- итоговые доли положительных и отрицательных отзывов.
        """
        from_year, to_year = years
        con = sqlite3.connect(CONNECTION)
        cur = con.cursor()
        id_bank = banks.index(bankName)
        if region[0] == '0 Вся Россия':
            string = ""
        else:
            string = "AND id_region IN ("
            for reg in region:
                string += f"{str(reg.split()[0])}, "
            string = string[:-2]
            string += ")"
        if bankName == 'Среднее по всем банкам':
            string2 = ''
        else:
            string2 = f" AND id_bank={id_bank} "
        string3 = f" AND year >= {from_year} AND year <= {to_year} "
        print(string + string2 + string3)
        convenience = len(cur.execute("SELECT rate FROM reviews WHERE c1=1 " + string + string2 + string3).fetchall())
        if convenience != 0:
            conveniencePositive = len(cur.execute("SELECT rate FROM reviews WHERE c1=1 " + string + string2 + string3 +
                                                  "AND rate in (4, 5)").fetchall())
            convenienceNegative = len(cur.execute("SELECT rate FROM reviews WHERE c1=1 " + string + string2 + string3 +
                                                  "AND rate in (1, 2)").fetchall())
        else:
            convenience, conveniencePositive, convenienceNegative = 1, 0, 0

        atm = len(
            cur.execute("SELECT rate FROM reviews WHERE c2=1 " + string + string2).fetchall())
        if atm != 0:
            atmPositive = len(cur.execute("SELECT rate FROM reviews WHERE c2=1 " + string + string2 + string3 +
                                          "AND rate in (4, 5)").fetchall())
            atmNegative = len(cur.execute("SELECT rate FROM reviews WHERE c2=1 " + string + string2 + string3 +
                                          "AND rate in (1, 2)").fetchall())
        else:
            atm, atmPositive, atmNegative = 1, 0, 0

        service = len(
            cur.execute("SELECT rate FROM reviews WHERE c3=1 " + string + string2).fetchall())
        if service != 0:
            servicePositive = len(cur.execute("SELECT rate FROM reviews WHERE c3=1 " + string + string2 + string3 +
                                              "AND rate in (4, 5)").fetchall())
            serviceNegative = len(cur.execute("SELECT rate FROM reviews WHERE c3=1 " + string + string2 + string3 +
                                              "AND rate in (1, 2)").fetchall())
        else:
            service, servicePositive, serviceNegative = 1, 0, 0

        staff = len(
            cur.execute("SELECT rate FROM reviews WHERE c4=1 " + string + string2).fetchall())
        if staff != 0:
            staffPositive = len(cur.execute("SELECT rate FROM reviews WHERE c4=1  " + string + string2 + string3+
                                            "AND rate in (4, 5)").fetchall())
            staffNegative = len(cur.execute("SELECT rate FROM reviews WHERE c4=1 " + string + string2 +
                                            "AND rate in (1, 2)").fetchall())
        else:
            staff, staffPositive, staffNegative = 1, 0, 0

        products = len(
            cur.execute("SELECT rate FROM reviews WHERE c5=1 " + string + string2).fetchall())
        if products != 0:
            productsPositive = len(cur.execute("SELECT rate FROM reviews WHERE c5=1 " + string + string2 + string3+
                                               "AND rate in (4, 5)").fetchall())
            productsNegative = len(cur.execute("SELECT rate FROM reviews WHERE c5=1 " + string + string2 + string3+
                                               "AND rate in (1, 2)").fetchall())
        else:
            products, productsPositive, productsNegative = 1, 0, 0

        remote = len(
            cur.execute("SELECT rate FROM reviews WHERE c6=1 " + string + string2).fetchall())
        if remote != 0:
            remotePositive = len(cur.execute("SELECT rate FROM reviews WHERE c6=1 " + string + string2 + string3 +
                                             "AND rate in (4, 5)").fetchall())

            remoteNegative = len(cur.execute("SELECT rate FROM reviews WHERE c6=1 " + string + string2 + string3 +
                                             "AND rate in (1, 2)").fetchall())
        else:
            remote, remotePositive, remoteNegative = 1, 0, 0

        # print("SELECT rate FROM reviews WHERE c6=1 " + string + string2 +
        #                                      "AND rate in (4, 5)")
        cur.close()
        con.close()
        resultPositive = conveniencePositive+atmPositive+servicePositive+staffPositive+productsPositive+remotePositive
        resultNegative = convenienceNegative+atmNegative+serviceNegative+staffNegative+productsNegative+remoteNegative
        result = resultPositive + resultNegative
        if(flag):
            return [
                [(conveniencePositive * 100) // convenience, (convenienceNegative * 100) // convenience],
                [(atmPositive * 100) // atm, (atmNegative * 100) // atm],
                [(servicePositive * 100) // service, (serviceNegative * 100) // service],
                [(staffPositive * 100) // staff, (staffNegative * 100) // staff],
                [(productsPositive * 100) // products, (productsNegative * 100) // products],
                [(remotePositive * 100) // remote, (remoteNegative * 100) // remote],
                [(resultPositive * 100) // result, (resultNegative * 100) // result],
            ]
        else:
            return [
                [conveniencePositive, convenienceNegative, (conveniencePositive * 100) // convenience, (convenienceNegative * 100) // convenience],
                [atmPositive, atmNegative, (atmPositive * 100) // atm, (atmNegative * 100) // atm],
                [servicePositive, serviceNegative, (servicePositive * 100) // service, (serviceNegative * 100) // service],
                [staffPositive, staffNegative, (staffPositive * 100) // staff, (staffNegative * 100) // staff],
                [productsPositive, productsNegative, (productsPositive * 100) // products, (productsNegative * 100) // products],
                [remotePositive, remoteNegative, (remotePositive * 100) // remote, (remoteNegative * 100) // remote],
                [resultPositive/result, resultNegative/result],
            ]

    def tornadoChart(self, bankName: str, list_categories: list, count: int, number_of_language: int):
        """
        Визуализация диаграммы в формате "торнадо" ("бабочка").
        bankName: str -- название банка
        list_categories: list -- список состоящий из пар процентного соотношения положительных и
        отрицательных отзывов по категориям
        count: int -- количество диаграмм в строке (необходимо для динамического подбора размеров диаграммы)

        return:
        fig : plotly.graph_objects.Figure -- построенная диаграмма
        """
        short_categories = ['Итог', 'УО', 'ATM', 'УC', 'П', 'ПиУ', 'ДКО'] if number_of_language == 0  \
            else ['Total', "CotO", "ATM", "LoS", "S", "P&S", "RSC"]
        chart_studio.tools.set_credentials_file(username='fedchenko.anastasiia', api_key='nSu1PDGAHBUXTnDTK8FB')
        convenience, atm, service, staff, products, remote, result = list_categories
        if bankName == "Среднее по всем банкам" and number_of_language == 1:
            bankName = "All banks"
        else:
            bankName = bankName if number_of_language == 0 else banks_en[banks.index(bankName) - 1]
            print(bankName)
            print('1111111')
        trace1 = {
            "name": LANGUAGES["tornado"][0][number_of_language],
            "type": "bar",
            "x": [result[1], convenience[1], atm[1], service[1], staff[1], products[1], remote[1]],
            "y": [1, 2, 3, 4, 5, 6, 7],
            "marker": {"color": "rgba(255, 0, 50, 1)"},
            "orientation": "h"
        }
        trace2 = {
            "name": LANGUAGES["tornado"][1][number_of_language],
            "type": "bar",
            "x": [result[0], convenience[0], atm[0], service[0], staff[0], products[0], remote[0]],
            "y": [1, 2, 3, 4, 5, 6, 7],
            "xaxis": "x2",
            "yaxis": "y2",
            "marker": {"color": "rgba(0, 255, 50, 1)"},
            "orientation": "h"
        }
        data = [trace1, trace2]
        layout = {
            "title": bankName,
            "width": 1200 // count,
            "xaxis": {
                "type": "linear",
                "range": [100, 0],
                "domain": [0, 0.5],
                # "autorange": True
            },
            "yaxis": {
                "type": "linear",
                "autorange": True,
                "tickmode": 'array',
                "tickvals": [1, 2, 3, 4, 5, 6, 7],
                "ticktext": short_categories
            },
            "height": 500,
            "xaxis2": {
                "type": "linear",
                "range": [0, 100],
                "anchor": "y2",
                "domain": [0.5, 1],
                # "autorange": True,
                "showticklabels": True
            },
            "yaxis2": {
                "type": "linear",
                "range": [0.5, 6],
                "anchor": "x2",
                "domain": [0, 1],
                "autorange": True,
                "showticklabels": False
            },
            "autosize": True,
            "showlegend": True,
            "barmode": "stack",
        }

        fig = go.Figure(data=data, layout=layout)
        return fig

    def tornadoChartAverage(self, bankName: str, regions: list, count: int, years: list, number_of_language: int):
        """
        Сбор данных для диаграммы в формате "торнадо" ("бабочка") для определенного банка по выбранным регионам.
        bankName: str -- название банка
        regions: list -- список выбранных регионов
        count: int -- количество диаграмм в строке (необходимо для динамического подбора размеров диаграммы)
        years: list -- период, за который нужно производить визуализацию

        return:
        fig : plotly.graph_objects.Figure -- построенная диаграмма
        """

        list_categories = self.getPositiveAndNegativeShareForCategories(bankName, regions, True, years)
        return self.tornadoChart(bankName, list_categories, count, number_of_language)

    def tornadoChartInBank(self, bankName: str, regions: list, count: int, years: list, number_of_language: int):
        """
        Сбор данных для диаграммы в формате "торнадо" ("бабочка") для определенного банка по выбранным регионам
        и прореживание(сравнивание со средним по всем категориям).
        прореживание — отбрасывание категорий, распределение которых с высокой вероятностью совпадает с распределением среднего
        bankName: str -- название банка
        regions: list -- список выбранных регионов
        count: int -- количество диаграмм в строке (необходимо для динамического подбора размеров диаграммы)
        years: list -- период, за который нужно производить визуализацию

        return:
        fig : plotly.graph_objects.Figure -- построенная диаграмма
        """
        convenience, atm, service, staff, products, remote, result = \
            self.getPositiveAndNegativeShareForCategories(bankName, regions, False, years)
        list_of_categories = [convenience, atm, service, staff, products, remote]
        print(list_of_categories)
        for category in list_of_categories:
            if not (category[0]==0 or category[1]==0):
                if (chi2_contingency([[category[0], category[1]],
                                      [result[0] * (category[0]+category[1]), result[1] * (category[0]+category[1])]])[1] > 0.05):
                    category[2] = 0
                    category[3] = 0
        list_categories = [[list_of_categories[0][2], list_of_categories[0][3]], \
                           [list_of_categories[1][2], list_of_categories[1][3]], \
                           [list_of_categories[2][2], list_of_categories[2][3]], \
                           [list_of_categories[3][2], list_of_categories[3][3]], \
                           [list_of_categories[4][2], list_of_categories[4][3]], \
                           [list_of_categories[5][2], list_of_categories[5][3]], \
                           [result[0]*100, result[1]*100]]
        print(list_of_categories)
        return self.tornadoChart(bankName, list_categories, count, number_of_language)

    def tornadoChartBetweenBanks(self, bankNames: list, regions: list, years: list, number_of_language: int):
        """
        Сбор данных для диаграммы в формате "торнадо" ("бабочка") для определенного банка по выбранным регионам
        и прореживание (сравнивание по каждой из категории с каждым банком).
        прореживание — отбрасывание категорий, распределение которых с высокой вероятностью
        совпадает с распределением категорий каждого из выбранных банков

        bankNames: list -- название банков
        regions: list -- список выбранных регионов
        years: list -- период, за который нужно производить визуализацию

        return:
        fig : plotly.graph_objects.Figure -- построенная диаграмма
        """
        banks = []
        categories = []
        res = []

        for i in range(len(bankNames)):
            res.append([])
            for j in range(7):
                res[i].append([])

        for bankName in bankNames:
            categories = self.getPositiveAndNegativeShareForCategories(bankName, regions, False, years)
            banks.append(categories)
        #pprint(banks)
        for c in range(0, len(categories) - 1):  # выбор категории, по которой будем проводить анализ
            flag_category_stays = False  # флаг того, что эта категория уже обнусена
            if_there_is_00 = False
            for k in range(0, len(banks)):
                if banks[k][c][0]==0 or banks[k][c][1]==0 or banks[k][c][2]==0 or banks[k][c][3]==0:
                    if_there_is_00 = True
            if not if_there_is_00:
                for i in range(0, len(banks)):  # выбор первого банка
                    for j in range(i + 1, len(banks)):  # выбор второго банка
                        if (chi2_contingency([[banks[j][c][0], banks[j][c][1]], \
                                              [(banks[i][c][2] / 100) * (banks[j][c][0] + banks[j][c][1]), \
                                               (banks[i][c][3] / 100) * (banks[j][c][0] + banks[j][c][1])]])[1] < 0.05):
                            flag_category_stays = True
                if flag_category_stays:
                    for d in range(len(bankNames)):
                        res[d][c].append(banks[d][c][2])
                        res[d][c].append(banks[d][c][3])
                else:
                    for d in range(len(bankNames)):
                        res[d][c].append(0)
                        res[d][c].append(0)
            else:
                for d in range(len(bankNames)):
                    res[d][c].append(banks[d][c][2])
                    res[d][c].append(banks[d][c][3])

        for d in range(len(bankNames)):
            res[d][6].append(banks[d][6][0] * 100)  # добавить проценты
            res[d][6].append(banks[d][6][1] * 100)
        return res

    def important_words_and_coefs(self, words: list, coefs: list):
        """
        Визуализация важных слов в категориях (на основе BinaryClassifierModel.key_words_for_categories())

        words : list -- список важных слов
        coefs : list -- коэффициенты важности слов

        return:
        fig : plotly.graph_objects.Figure -- построенная диаграмма
        """
        fig = px.bar(x=[
            coefs
        ],
            y=words,
            labels={
                'x': 'coefficient',
                'y': 'words'},
            height=750,
            color=["purple"]*20,
            color_discrete_map="identity",
            # title="Средняя оценка по всем банкам",
            text=[abs(round(x, 4)) for x in coefs])
        return fig
