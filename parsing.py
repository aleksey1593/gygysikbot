from bs4 import BeautifulSoup
import requests
import re

def uznat():
    url = 'http://www.nbrb.by/statistics/rates/ratesdaily.asp'
    page = requests.get(url)
    new_course = {}
    soup = BeautifulSoup(page.text, "html.parser")
    course = soup.findAll('tr')
    for i in range(len(course)):
        if course[i].find('span', class_='text') is not None:
            element = course[i].text
            if 'USD' in element:
                spisok = element.split('\n')
                new_course['USD'] = spisok[9]
            if 'EUR' in element:
                spisok = element.split('\n')
                new_course['EUR'] = spisok[9]
    return new_course

def banki_kursi(type, valuta):
    if type == 'продажа' and valuta == 'USD':
        url = 'https://finance.tut.by/kurs/minsk/dollar/?sortBy=buy&sortDir=down&summa=100&bn_rate=0'
    elif type == 'покупка' and valuta == 'USD':
        url = 'https://finance.tut.by/kurs/minsk/dollar/?sortBy=sell&sortDir=up&summa=100&bn_rate=0'
    elif type == 'продажа' and valuta == 'EUR':
        url ='https://finance.tut.by/kurs/minsk/euro/?sortBy=buy&sortDir=down&summa=100&bn_rate=0'
    elif type == 'покупка' and valuta == 'EUR':
        url = 'https://finance.tut.by/kurs/minsk/euro/?sortBy=sell&sortDir=up&summa=100&bn_rate=0'
    else:
        return f'Ошибка ввода'
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        mesto = soup.find('table', class_="tbl-lite banks-table")
        course = mesto.findAll('span')
        vse_banki = mesto.findAll('div', class_='cc-c')
        curs = []
        curs_itog = []
        banki = []
        adres = []
        itog = []
        for i in range(len(course)):
            krs = course[i].text
            if not re.match(r'\d[.]\d+', krs[0:6]):
                continue
            curs.append(krs[0:6])
        for i in range(0,10,2):
            if type == "продажа":
                curs_itog.append(curs[i])
            bank = vse_banki[i].find('a')
            banki.append(bank.text)
        for i in range(1,10,2):
            if type == "покупка":
                curs_itog.append(curs[i])
            mestopolozenie = vse_banki[i].find('a')
            adres.append(mestopolozenie.text)
        for i in range(5):
            element = f'{banki[i]} {adres[i]} курс {curs_itog[i]}'
            itog.append(element)
    except BaseException:
        itog = f'Ошибка'
    return itog