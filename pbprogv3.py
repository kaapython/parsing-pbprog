import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver


def get_data():
    """
        Функция парсинга каталога пунктов опорно-межевых сетей (геоточек) поиск и получение координат
        сесурс: https://pbprog.ru/
        версия: 3
    """
    data = points_1 = points_2 = points_3 = points_4 = []

    print(), print('* * * * * The start of parsing * * * * *')
    print(f"* * * * *         {time.strftime('%R')}        * * * * *"), print()

    firefox_options = Options()
    firefox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=firefox_options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get('https://pbprog.ru/webservices/oms/')

    driver.find_element(By.LINK_TEXT, 'Войти').click()
    driver.find_element(By.NAME, 'USER_LOGIN').send_keys('login')
    driver.find_element(By.NAME, 'USER_PASSWORD').send_keys('psswd')
    driver.find_element(By.NAME, 'Login').click()
    print('* * * Clicked Login'), print()
    time.sleep(10)

    # Получение списка объектов Иркутской области
    points_1.append(driver.find_element(By.CLASS_NAME, "schema").text.split('\n')[38])
    driver.find_element(By.LINK_TEXT, points_1[0]).click()
    time.sleep(5)
    print('* * * Clicked points_1', points_1[0])

    e1 = driver.find_element(By.ID, 's38')
    points_2.append(e1.text.split('\n'))
    print('points_2 >', points_2[0]), print()

    for point_2 in points_2[0]:
        link = driver.find_element(By.LINK_TEXT, point_2)
        link.click()
        time.sleep(3)
        name = link.text
        print('* * * Clicked points_2', name)

        e2 = driver.find_element(By.ID, f's{name[:2]}_{name[3:5]}')
        points_3.append(e2.text.split('\n')[1])
        print('points_3 >', points_3), print()

        for point in range(len(points_3)):
            driver.find_element(By.LINK_TEXT, points_3[point]).click()
            time.sleep(5)
            print('* * * Clicked point', points_3[point])
            points_4.clear()
            print('clear points_4 > ', points_4)
            print('point > ', f's{points_3[point][:2]}_{points_3[point][3:len(points_3[point])]}_')

            e3 = driver.find_element(By.ID, f's{points_3[point][:2]}_{points_3[point][3:len(points_3[point])]}_')
            points_4.append(e3.text.split('\n'))
            points_4 = points_4[0]
            print('points_4 >', points_4, f's{points_3[point][:2]}_{points_3[point][3:len(points_3[point])]}_')

            for p in points_4:
                driver.find_element(By.LINK_TEXT, p).click()
                time.sleep(5)

                e5 = driver.find_elements(By.XPATH, '//div[@id="map"]//table[@class="data-table"]')
                for i in e5:
                    if len(i.text) != 0:
                        data.append(i.text.split('\n'))
                print('data >', data), print()
                time.sleep(3)
                driver.find_element(By.ID, 'close').click()
                print('* * * * * Clicked close table * * * * *'), print()

                if len(data) != 0:
                    if len(data[0]) == 6:
                        with open(f'files/{name[6:].split(" ")[0]}.txt', 'a') as file:
                            print('len_data >', len(data[0]), len(data[0]) == 6), print()
                            for i in range(len(data)):
                                if len(data[i]) != 1:
                                    d1 = data[i][3].replace('Координаты точки в местной СК, метры (X - вертикально, '
                                                            'Y - горизонтально)', 'Координаты точки в местной СК\t')
                                    file.write(
                                        f'{data[i][1]} \t {data[i][2]} \t {d1} \t {data[i][4]} \t {data[i][5]} \n')
                                    print('* * * * * Written to a file * * * * *'), print()
                                else:
                                    print({i: data[i]})

                            print('* * * * * Clear data * * * * *'), print()
                    if len(data[0]) == 8:
                        with open(f'files/{name[6:].split(" ")[0]}.txt', 'a') as file:
                            print('len_data >', len(data[0]), len(data[0]) == 8), print()
                            for i in range(len(data)):
                                if len(data[i]) != 1:
                                    d1 = data[i][4].replace('Координаты точки в местной СК, метры (X - вертикально, '
                                                            'Y - горизонтально)', 'Координаты точки в местной СК\t')
                                    d2 = data[i][5].replace('Координаты точки в СК WGS-84 в проекции Меркатора, метры '
                                                            '(Y - вертикально, X - горизонтально)',
                                                            'Координаты точки в СК '
                                                            'WGS-84 в проекции Меркатора\t')
                                    d3 = data[i][6].replace('Координаты точки в СК WGS-84, градусы и доли '
                                                            '(широта - вертикально, долгота - горизонтально)',
                                                            'Координаты точки в СК WGS-84\t')
                                    file.write(
                                        f"{data[i][1]}\t {data[i][2]}\t {data[i][3]}\t {d1}\t {d2}\t {d3}\t {data[i][7]}\n")
                                    print('* * * * * Written to a file * * * * *')
                                else:
                                    print({i: data[i]})
                    if len(data[0]) == 7:
                        with open(f'files/{name[6:].split(" ")[0]}.txt', 'a') as file:
                            print('len_data >', len(data[0]), len(data[0]) == 7), print()
                            for i in range(len(data)):
                                if len(data[i]) != 1:
                                    d1 = data[i][4].replace('Координаты точки в местной СК, метры (X - вертикально, '
                                                            'Y - горизонтально)', 'Координаты точки в местной СК\t')
                                    d2 = data[i][5].replace('Координаты точки в СК WGS-84 в проекции Меркатора, метры '
                                                            '(Y - вертикально, X - горизонтально)',
                                                            'Координаты точки в СК '
                                                            'WGS-84 в проекции Меркатора\t')
                                    d3 = data[i][6].replace('Координаты точки в СК WGS-84, градусы и доли '
                                                            '(широта - вертикально, долгота - горизонтально)',
                                                            'Координаты точки в СК WGS-84\t')
                                    file.write(
                                        f"{data[i][1]}\t {data[i][2]}\t {data[i][3]}\t {d1}\t {d2}\t {d3}\n")
                                    print('* * * * * Written to a file * * * * *')
                                else:
                                    print({i: data[i]})

                data.clear()
                print('* * * * * Clear data * * * * *'), print()

        points_3.clear()
        print('clear points_3 >', points_3), print()
        print('* * * * * END * * * * *'), print()
    driver.quit()


get_data()
