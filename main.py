from PIL import Image
from urllib.request import urlopen
from xml.dom import minidom
import sys
import requests
import pandas as pd

# Task №1
# один из файлов некорректно читается и не загружается, поэтому первое задание выполнено наполовину 
# выполнена загрузка файла и сформирована промежуточная таблица для дальнейшего использования данных
# чтение xml по url
url = urlopen('http://stripmag.ru/datafeed/p5s_full_stock.xml')
mydoc = minidom.parse(url)

# чтение полей product, price, assort
product = mydoc.getElementsByTagName('product')
price = mydoc.getElementsByTagName('price')
assort = mydoc.getElementsByTagName('assort')

# вспомогательные списки для создания таблицы
list_prodid = list()
list_price_rp = list()
list_price_brp = list()
list_price_wp = list()
list_price_bwp = list()
list_price_d = list()
list_sklad = list()
list_aID = list()
list_barcode = list()
list_ShippingDate = list()

# заполнение списков
i = 0
for elem in product:
    list_prodid.append(product[i].attributes['prodID'].value)
    i += 1

i = 0
for elem in price:
    list_price_rp.append(price[i].attributes['RetailPrice'].value)
    list_price_brp.append(price[i].attributes['BaseRetailPrice'].value)
    list_price_wp.append(price[i].attributes['WholePrice'].value)
    list_price_bwp.append(price[i].attributes['BaseWholePrice'].value)
    list_price_d.append(price[i].attributes['Discount'].value)
    i += 1

i = 0
for elem in assort:
    list_sklad.append(assort[i].attributes['sklad'].value)
    list_aID.append(assort[i].attributes['aID'].value)
    list_barcode.append(assort[i].attributes['barcode'].value)
    list_ShippingDate.append(assort[i].attributes['ShippingDate'].value)
    i += 1

data1 = {'prodID': list_prodid, 'RetailPrice': list_price_rp, 'BaseRetailPrice': list_price_brp,
         'WholePrice': list_price_wp, 'BaseWholePrice': list_price_bwp, 'Discount': list_price_d}
data2 = {'sklad': list_sklad, 'aID': list_aID, 'barcode': list_barcode, 'ShippingDate': list_ShippingDate}
# создание таблиц по product price и assort для дальнейшего использования
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
# вывод таблиц
# print(df1)
# print(df2)


# Task №2
# функция для наложения плашки поверх картинку
def im_to_im():
    #функция для чтения картинки по url
    def url_to_img(url):
        try:
            resp = requests.get(url, stream=True).raw
        except requests.exceptions.RequestException as e:
            sys.exit(1)

        name = input('Введите название для картинки: ')

        try:
            img = Image.open(resp)
        except IOError:
            print("Не удалось открыть")
            sys.exit(1)
        # сохранение считанных картинок по url
        img.save(name)

    url_pl = 'http://alitair.1gb.ru/test_prog_plashki/benefit.png'
    url_img = 'http://alitair.1gb.ru/test_prog_plashki/106044_benefit.jpg'

    # url_to_img(url_pl)  # name = pl.png
    # url_to_img(url_img)  # name = img.png

    pl = Image.open("pl.png")
    img = Image.open("img.png")

    # для наложения по центру
    im_width = round((pl.width - img.width) / 2)
    im_height = round((pl.height - img.height) / 2)

    position = (im_width, im_height)

    pl.paste(img, position)

    # сохранение
    pl.save("Fin_image.png")


im_to_im()
