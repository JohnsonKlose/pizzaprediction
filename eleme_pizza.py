# -*- coding: utf-8 -*-
import requests
import numpy
import time
import json
import sys
import csv
import codecs


reload(sys)
sys.setdefaultencoding('utf-8')


def is_pizza(str):
    if '披萨' in str:
        return True
    if '比萨' in str:
        return True
    if 'Pizza' in str:
        return True
    if 'pizza' in str:
        return True
    return False


filename = 'xinjiekou.csv'
f = open(filename, 'w')
f.write(codecs.BOM_UTF8)
writer = csv.writer(f)
writer.writerow(['shop_id', 'shop_address', 'shop_name', 'delivery_fee', 'latitude', 'longitude', 'opening_hours',
                 'recent_order_num', 'shop_rating', 'shop_compare_rating', 'shop_food_score', 'shop_positive_rating',
                 'shop_service_score', 'shop_star_level', 'menu_name', 'item_id', 'item_description', 'item_month_sales',
                 'item_name', 'item_rating', 'item_rating_count', 'item_satisfy_count', 'item_satisfy_rate'])

search_geohash = 'wtsw9yrc72y'  # 南京
# search_geohash = 'wtw3sjq6n6um'
search_keyword = '新街口'
search_url = 'https://www.ele.me/restapi/v2/pois?extras%5B%5D=count&geohash=' + search_geohash \
             + '&keyword=' + search_keyword + '&limit=20&type=nearby'

cookie = {'cookie': 'ubt_ssid=labx9txj4072ybh58eb61rr28hatqpgj_2018-03-12; _utrace=1b1600d0736abe9a21bd833cec1df675_2018-03-12; track_id=1521816690|6511ab1a4330cafc052e81e1efe6e27543487a5a19c4b5934a|438972856c9a603c574dedc2e88980b5; USERID=17395205; SID=9tlXlbhOjlYBMZcY9CDEoAJ8tvykR7DyVtUA'}

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8'}

search_ = requests.get(search_url, headers=head)
time.sleep(2 + numpy.random.randint(0, 3))
search_json = json.loads(search_.text)

count_max = 0
search_result = {}
for res in search_json:
    if res['count'] > count_max:
        count_max = res['count']
        search_result = res
# print search_result['name']

for i in range(0, 10):
    shop_url = 'https://www.ele.me/restapi/shopping/restaurants?geohash=' + str(search_result['geohash']) + \
               '&latitude=' + str(search_result['latitude']) + '&limit=24&longitude=' + str(search_result['longitude']) + \
               '&offset=' + str(i*24) + '&restaurant_category_ids%5B%5D=3&terminal=web'
    shop_ = requests.get(shop_url, headers=head, cookies=cookie)
    time.sleep(2 + numpy.random.randint(0, 3))
    shop_json = json.loads(shop_.text)
    if len(shop_json) == 0:
        break
    for shop in shop_json:

        # 首先判断是否为披萨店
        json_id = []
        for flv in shop['flavors']:
            json_id.append(flv['id'])
        if 211 not in json_id:
            continue

        # 店铺信息
        shop_id = shop['id']
        print shop_id
        shop_address = shop['address']
        shop_name = shop['name']
        shop_delivery_fee = shop['float_delivery_fee']
        shop_latitude = shop['latitude']
        shop_longitude = shop['longitude']
        shop_opening_hours = shop['opening_hours']
        shop_recent_order_num = shop['recent_order_num']
        shop_rating = shop['rating']

        rating_url = 'https://www.ele.me/restapi/ugc/v1/restaurants/' + str(shop_id) + \
                     '/rating_scores?latitude=' + str(search_result['latitude']) + '&longitude=' + \
                     str(search_result['longitude'])
        rating_ = requests.get(rating_url)
        time.sleep(2 + numpy.random.randint(0, 3))
        rating_json = json.loads(rating_.text)
        if len(rating_json) != 0:
            shop_compare_rating = rating_json['compare_rating']
            shop_food_score = rating_json['food_score']
            shop_positive_rating = rating_json['positive_rating']
            shop_service_score = rating_json['service_score']
            shop_star_level = rating_json['star_level']
        else:
            continue

        pizza_url = 'https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=' + str(shop_id) + '&terminal=web'
        head_pizza = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https://www.ele.me/shop/' + str(shop_id)
        }
        pizza_ = requests.get(pizza_url)
        time.sleep(2 + numpy.random.randint(0, 3))
        pizza_json = json.loads(pizza_.text)
        for menu_json in pizza_json:
            if is_pizza(menu_json['name']):

                # 目录信息
                menu_name = menu_json['name']

                food_json = menu_json['foods']
                for foods in food_json:

                    # 单品信息
                    foods_id = foods['item_id']
                    foods_description = foods['description']
                    foods_month_sales = foods['month_sales']
                    foods_name = foods['name']
                    foods_rating = foods['rating']
                    foods_rating_count = foods['rating_count']
                    foods_satisfy_count = foods['satisfy_count']
                    foods_satisfy_rate = foods['satisfy_rate']
                    print foods_name
                    writer.writerow([shop_id, shop_address, shop_name, shop_delivery_fee, shop_latitude, shop_longitude,
                                     shop_opening_hours, shop_recent_order_num, shop_rating, shop_compare_rating,
                                     shop_food_score, shop_positive_rating, shop_service_score, shop_star_level,
                                     menu_name, foods_id, foods_description, foods_month_sales, foods_name,
                                     foods_rating, foods_rating_count, foods_satisfy_count, foods_satisfy_rate])
f.close()