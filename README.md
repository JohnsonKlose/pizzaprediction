# pizzaprediction  
此项目爬取饿了么外卖网站的披萨商品信息，包括店铺坐标、店铺评星、店铺订单量、单品描述、单品销量、单品评星等信息，通过对商品描述进行分词，统计词频提取披萨商品的特征，运用神经网络和XGBoost两种机器学习算法，构建披萨商品预测模型。

## 爬虫思路
- 分析饿了么官网地址关键字搜索:  
以在南京市搜索“新街口”为例，抓包查看到地址关键字搜索的访问地址为[https://www.ele.me/restapi/v2/pois?extras%5B%5D=count&geohash=wtsw9yrc72y&keyword=%E6%96%B0%E8%A1%97%E5%8F%A3&limit=20&type=nearby](https://www.ele.me/restapi/v2/pois?extras%5B%5D=count&geohash=wtsw9yrc72y&keyword=%E6%96%B0%E8%A1%97%E5%8F%A3&limit=20&type=nearby)  
分析url我们可以发现，关键字内容存放在参数keyword中，这样构造请求地址后就可以爬取到地址信息了，我们这里默认选择地址信息中店铺数量最多的地址。  
**Tips:**需要注意的是如果爬取其他城市的话，需要更换geohash后的内容。  
- 分析店铺搜索结果页面  
![shopsearch](http://oswrmk9hd.bkt.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-06-05%20%E4%B8%8B%E5%8D%889.37.24.png)
选择某一地址后，进入店铺页面，选择“美食-汉堡披萨”类，抓包查看此类店铺搜索的访问地址为[https://www.ele.me/restapi/shopping/restaurants?geohash=wtsqqbuz1u87&latitude=32.041479&limit=24&longitude=118.779792&offset=0&restaurant_category_ids%5B%5D=3&terminal=web](https://www.ele.me/restapi/shopping/restaurants?geohash=wtsqqbuz1u87&latitude=32.041479&limit=24&longitude=118.779792&offset=0&restaurant_category_ids%5B%5D=3&terminal=web)  
分析url，geohash为地理编码信息，与上一个地址关键字搜索url相同；latitude和longitude为经纬度信息，可以通过地址搜索结果获取；offset为翻页信息，查看爬取数据结果可以发现每页有24条数据，因此可以迭代offset值获取所有的店铺信息。  
构造了请求地址后就可以爬取店铺信息了，需要注意的是，本项目只需要爬取披萨门店就可以了，因此可以在获取店铺信息前判断该门店是否是披萨门店，即判断店铺id中是否含有211，如果没有211就直接跳过爬取下一个店铺。  
```
for i in range(0, 10):  
	# search_result为爬取地址信息的具体内容
    shop_url = 'https://www.ele.me/restapi/shopping/restaurants?geohash=' + str(search_result['geohash']) + '&latitude=' + str(search_result['latitude']) + '&limit=24&longitude=' + str(search_result['longitude']) + '&offset=' + str(i*24) + '&restaurant_category_ids%5B%5D=3&terminal=web'  
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
        shop_address = shop['address']  
        shop_name = shop['name']  
        shop_delivery_fee = shop['float_delivery_fee']  
        shop_latitude = shop['latitude']  
        shop_longitude = shop['longitude']  
        shop_opening_hours = shop['opening_hours']  
        shop_recent_order_num = shop['recent_order_num']  
        shop_rating = shop['rating']  
```  
- 分析店铺页面爬取披萨品类信息  
![itemcategory](http://oswrmk9hd.bkt.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-06-05%20%E4%B8%8B%E5%8D%8810.42.52.png)
查看某个店铺的页面，可以看到页面中对所有商品做了一个分类，分类内容会有沙拉、披萨、饮料等等，因此我们可以先判断该分类是否为披萨品类，然后再爬取改分类下的披萨商品，判断披萨品类方法如下。  
```
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
```  
找到披萨分类后遍历所有披萨商品，爬取披萨商品的信息包括商品描述、月销量、名称、评星、评星数等，最终结果保存在csv文件中。  
```
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
```  