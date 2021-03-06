# pizzaprediction  
此项目爬取饿了么外卖网站的披萨商品信息，包括店铺坐标、店铺评星、店铺订单量、单品描述、单品销量、单品评星等信息，通过对商品描述进行分词，统计词频提取披萨商品的特征，运用神经网络和XGBoost两种机器学习算法，构建披萨商品预测模型。

## 爬虫思路
- 分析饿了么官网地址关键字搜索:  
以在南京市搜索“新街口”为例，抓包查看到地址关键字搜索的访问地址为[https://www.ele.me/restapi/v2/pois?extras%5B%5D=count&geohash=wtsw9yrc72y&keyword=%E6%96%B0%E8%A1%97%E5%8F%A3&limit=20&type=nearby](https://www.ele.me/restapi/v2/pois?extras%5B%5D=count&geohash=wtsw9yrc72y&keyword=%E6%96%B0%E8%A1%97%E5%8F%A3&limit=20&type=nearby)  
分析url我们可以发现，关键字内容存放在参数keyword中，这样构造请求地址后就可以爬取到地址信息了，我们这里默认选择地址信息中店铺数量最多的地址。  
**Tips:** 需要注意的是如果爬取其他城市的话，需要更换geohash后的内容。  
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

## 数据处理
- 数据清洗  
  因为不同的地理位置覆盖的范围可能重叠，因此我们爬到的店铺可能存在重复，所以我们需要将重复的数据去除，可以根据item_id去除重复数据  
  ```
  data = data.drop_duplicates(['item_id'])
  ```  
  同时，评星为0的数据对我们来说意义也不大，这些大多是销量很低还没有人评星的商品，可以视为离群数据将其取出  
  ```
  data = data[data['item_rating'] > 0]
  ```  
- 自然语言处理  
  为了提取商品原料的信息内容，将爬取到的商品描述信息进行分词处理，使用的是jieba库  
  ```
  def jieba_cut(word):
      s = jieba.cut(word)
      s = [word.encode('utf-8') for word in list(s)]
      stoplist = {}.fromkeys([line.strip() for line in open("./stopwords.txt")])
      segs = [word for word in list(s) if word not in stoplist]
      return segs
  ```  
  将分词的结果进行词频统计，使用pyecharts库将词频统计结果通过词云图可视化  
  ```
  def draw_word_cloud(word_data):
      from pyecharts import WordCloud
      word = []
      value = []
      for (k, v) in word_data.items():
          if v < 50:
              del word_data[k]
          else:
              word.append(k)
              value.append(v)
          wordcloud = WordCloud(width=1300, height=620)
          wordcloud.add("", word, value, word_size_range=[5, 1000], shape='diamond')
          wordcloud.render("./wordcloud.html")
  ```  
  ![wordcloud](http://oswrmk9hd.bkt.clouddn.com/wordcloud12.png)
  可以看到，词频较高的词有牛肉、鸡肉、培根、奶酪等，这些都是我们希望获得的披萨原料和风味，但是也有一些词，比如纸巾、风味、超级等没有多大意义的词，这里展示一下词频排在前30的有哪些词  

  词 | 词频  |:-|:-|
  芝士 | 2224
  披萨 | 1292
  寸 | 1018
  菠萝 | 826
  青椒 | 823
  牛肉 | 755
  酱 | 748
  火腿 | 737
  洋葱 | 718
  原料 | 666
  培根 | 641
  比萨 | 639
  蘑菇 | 603
  里拉 | 557
  马苏 | 515
  搭配 | 443
  12 | 413
  面团 | 409
  榴莲 | 399
  美味 | 395
  肠 | 389
  玉米 | 381
  鸡肉 | 374
  腊肉 | 329
  提供 | 325
  纸巾 | 325
  奶酪 | 308
  蔬菜 | 307
  香 | 288
  香肠 | 284
  海鲜 | 277

  可以发现，芝士的词频遥遥领先，果然芝士就是腻酿！！  
  其中发现了12这个有趣的高频词，其实是很多披萨商品是12寸的，因此12的词频就很高。可以看到分词结果还是比较混乱的，因此我将所有词频高于5且对商品描述有意义的词进行逐一分类，共分为风味、口味、烹制方法、蔬菜类、荤菜类、水果类、海鲜水产类、辅料佐料类。

  <table>
  	<thead>
  		<tr>
  			<th>大类</th>
  			<th>子类</th>
  			<th>词</th>
  		</tr>
  	</thead>
	<tr>
		<td rowspan=31>风味</td>
		<td rowspan=2>热带风味</td>
		<td>夏威夷</td>
	</tr>
	<tr>
		<td>热带</td>
	</tr>
	<tr>
		<td rowspan=7>意式风味</td>
		<td>意式</td>
	</tr>
	<tr>
		<td>意大利</td>
	</tr>
	<tr>
		<td>那不勒斯</td>
	</tr>
	<tr>
		<td>博洛尼亚</td>
	</tr>
	<tr>
		<td>西西里</td>
	</tr>
	<tr>
		<td>贝贝罗尼</td>
	</tr>
	<tr>
		<td>罗马</td>
	</tr>
	<tr>
		<td rowspan=3>东南亚风味</td>
		<td>泰国</td>
	</tr>
	<tr>
		<td>泰式</td>
	</tr>
	<tr>
		<td>马来西亚</td>
	</tr>
	<tr>
		<td>墨西哥风味</td>
		<td>墨西哥</td>
	</tr>
	<tr>
		<td rowspan=2>奥尔良风味</td>
		<td>奥尔良</td>
	</tr>
	<tr>
		<td>新奥尔良</td>
	</tr>
	<tr>
		<td rowspan=2>澳洲风味</td>
		<td>澳洲</td>
	</tr>
	<tr>
		<td>新西兰</td>
	</tr>
	<tr>
		<td>法式风味</td>
		<td>法国</td>
	</tr>
	<tr>
		<td rowspan=2>美式风味</td>
		<td>美国</td>
	</tr>
	<tr>
		<td>纽约</td>
	</tr>
	<tr>
		<td>荷兰风味</td>
		<td>荷兰</td>
	</tr>
	<tr>
		<td rowspan=2>德式风味</td>
		<td>德式</td>
	</tr>
	<tr>
		<td>德国</td>
	</tr>
	<tr>
		<td>台湾风味</td>
		<td>台湾</td>
	</tr>
	<tr>
		<td rowspan=2>韩式风味</td>
		<td>韩国</td>
	</tr>
	<tr>
		<td>韩式</td>
	</tr>
	<tr>
		<td>日式风味</td>
		<td>日式</td>
	</tr>
	<tr>
		<td rowspan=2>中式风味</td>
		<td>京味</td>
	</tr>
	<tr>
		<td>韩式</td>
	</tr>
	<tr>
		<td>海陆风味</td>
		<td>海陆</td>
	</tr>
	<tr>
		<td>全素风味</td>
		<td>全素</td>
	</tr>
	<tr>
		<td rowspan=31>口味</td>
		<td rowspan=6>脆</td>
		<td>香脆</td>
	</tr>
	<tr>
		<td>脆爽</td>
	</tr>
	<tr>
		<td>松脆</td>
	</tr>
	<tr>
		<td>清脆</td>
	</tr>
	<tr>
		<td>薄脆</td>
	</tr>
	<tr>
		<td>酥脆</td>
	</tr>
	<tr>
		<td rowspan=2>鲜</td>
		<td>鲜美</td>
	</tr>
	<tr>
		<td>香鲜</td>
	</tr>
	<tr>
		<td>酸</td>
		<td>酸甜</td>
	</tr>
	<tr>
		<td rowspan=3>甜</td>
		<td>酸甜</td>
	</tr>
	<tr>
		<td>香甜</td>
	</tr>
	<tr>
		<td>甜辣</td>
	</tr>
	<tr>
		<td rowspan=5>辣</td>
		<td>微辣</td>
	</tr>
	<tr>
		<td>香辣</td>
	</tr>
	<tr>
		<td>麻辣</td>
	</tr>
	<tr>
		<td>辣爽</td>
	</tr>
	<tr>
		<td>甜辣</td>
	</tr>
	<tr>
		<td rowspan=3>醇</td>
		<td>香醇</td>
	</tr>
	<tr>
		<td>醇香</td>
	</tr>
	<tr>
		<td>醇厚</td>
	</tr>
	<tr>
		<td rowspan=3>清</td>
		<td>清甜</td>
	</tr>
	<tr>
		<td>清新</td>
	</tr>
	<tr>
		<td>清脆</td>
	</tr>
	<tr>
		<td rowspan=2>柔</td>
		<td>柔韧</td>
	</tr>
	<tr>
		<td>柔嫩</td>
	</tr>
	<tr>
		<td rowspan=6>香</td>
		<td>果香</td>
	</tr>
	<tr>
		<td>芝香</td>
	</tr>
	<tr>
		<td>五香</td>
	</tr>
	<tr>
		<td>香甜</td>
	</tr>
	<tr>
		<td>香鲜</td>
	</tr>
	<tr>
		<td>浓香</td>
	</tr>
	<tr>
		<td rowspan=16>烹制方法</td>
		<td rowspan=2>薄底</td>
		<td>薄底</td>
	</tr>
	<tr>
		<td>薄饼</td>
	</tr>
	<tr>
		<td>厚底</td>
		<td>厚底</td>
	</tr>
	<tr>
		<td>铁盘</td>
		<td>铁盘</td>
	</tr>
	<tr>
		<td rowspan=7>烤制</td>
		<td>烘烤</td>
	</tr>
	<tr>
		<td>烤</td>
	</tr>
	<tr>
		<td>BBQ</td>
	</tr>
	<tr>
		<td>烤制</td>
	</tr>
	<tr>
		<td>烧烤</td>
	</tr>
	<tr>
		<td>现烤</td>
	</tr>
	<tr>
		<td>烤肉</td>
	</tr>
	<tr>
		<td>岩烧</td>
		<td>岩烧</td>
	</tr>
	<tr>
		<td>炭烧</td>
		<td>炭烧</td>
	</tr>
	<tr>
		<td>腌制</td>
		<td>腌制</td>
	</tr>
	<tr>
		<td>焗烧</td>
		<td>焗</td>
	</tr>
	<tr>
		<td>蜜汁</td>
		<td>蜜汁</td>
	</tr>
	<tr>
		<td rowspan=44>蔬菜类</td>
		<td rowspan=7>菜椒</td>
		<td>彩椒</td>
	</tr>
	<tr>
		<td>青椒</td>
	</tr>
	<tr>
		<td>红椒</td>
	</tr>
	<tr>
		<td>红彩椒</td>
	</tr>
	<tr>
		<td>黄彩椒</td>
	</tr>
	<tr>
		<td>灯笼椒</td>
	</tr>
	<tr>
		<td>甜椒</td>
	</tr>
	<tr>
		<td rowspan=3>辣椒</td>
		<td>脆椒</td>
	</tr>
	<tr>
		<td>辣椒</td>
	</tr>
	<tr>
		<td>尖椒</td>
	</tr>
	<tr>
		<td>橄榄</td>
		<td>橄榄</td>
	</tr>
	<tr>
		<td rowspan=2>洋葱</td>
		<td>洋葱</td>
	</tr>
	<tr>
		<td>onion</td>
	</tr>
	<tr>
		<td>京葱</td>
		<td>京葱</td>
	</tr>
	<tr>
		<td>青葱</td>
		<td>青葱</td>
	</tr>
	<tr>
		<td rowspan=3>玉米</td>
		<td>玉米</td>
	</tr>
	<tr>
		<td>玉米片</td>
	</tr>
	<tr>
		<td>玉米粒</td>
	</tr>
	<tr>
		<td rowspan=2>荞麦</td>
		<td>荞麦</td>
	</tr>
	<tr>
		<td>荞麦面</td>
	</tr>
	<tr>
		<td rowspan=2>黄瓜</td>
		<td>黄瓜</td>
	</tr>
	<tr>
		<td>酸黄瓜</td>
	</tr>
	<tr>
		<td rowspan=3>番茄</td>
		<td>西红柿</td>
	</tr>
	<tr>
		<td>番茄</td>
	</tr>
	<tr>
		<td>蕃茄</td>
	</tr>
	<tr>
		<td rowspan=3>菌菇</td>
		<td>蘑菇</td>
	</tr>
	<tr>
		<td>松露菌</td>
	</tr>
	<tr>
		<td>褐菇</td>
	</tr>
	<tr>
		<td>青豆</td>
		<td>青豆</td>
	</tr>
	<tr>
		<td>芦笋</td>
		<td>芦笋</td>
	</tr>
	</tr>
	<tr>
		<td>莴笋</td>
		<td>莴笋</td>
	</tr>
	<tr>
		<td>西葫芦</td>
		<td>西葫芦</td>
	</tr>
	<tr>
		<td>南瓜</td>
		<td>南瓜</td>
	</tr>
	<tr>
		<td>香菜</td>
		<td>香菜</td>
	</tr>
	<tr>
		<td>西兰花</td>
		<td>西兰花</td>
	</tr>
	<tr>
		<td rowspan=2>藕</td>
		<td>藕</td>
	</tr>
	<tr>
		<td>藕片</td>
	</tr>
	<tr>
		<td>茄子</td>
		<td>茄子</td>
	</tr>
	<tr>
		<td rowspan=5>土豆</td>
		<td>土豆</td>
	</tr>
	<tr>
		<td>土豆片</td>
	</tr>
	<tr>
		<td>薯角</td>
	</tr>
	<tr>
		<td>薯条</td>
	</tr>
	<tr>
		<td>脆薯</td>
	</tr>
	<tr>
		<td>红薯</td>
		<td>红薯</td>
	</tr>
	<tr>
		<td rowspan=30>荤菜类</td>
		<td>培根</td>
		<td>培根</td>
	</tr>
	<tr>
		<td rowspan=2>牛肉</td>
		<td>牛肉</td>
	</tr>
	<tr>
		<td>牛排</td>
	</tr>
	<tr>
		<td rowspan=6>鸡肉</td>
		<td>鸡肉</td>
	</tr>
	<tr>
		<td>烤鸡</td>
	</tr>
	<tr>
		<td>鸡腿肉</td>
	</tr>
	<tr>
		<td>鸡胸</td>
	</tr>
	<tr>
		<td>鸡胸肉</td>
	</tr>
	<tr>
		<td>鸡丁</td>
	</tr>
	<tr>
		<td rowspan=2>猪肉</td>
		<td>猪肉</td>
	</tr>
	<tr>
		<td>里脊</td>
	</tr>
	<tr>
		<td>鸭肉</td>
		<td>鸭肉</td>
	</tr>
	<tr>
		<td rowspan=2>烤鸭</td>
		<td>北京烤鸭</td>
	</tr>
	<tr>
		<td>烤鸭</td>
	</tr>
	<tr>
		<td>羊肉</td>
		<td>羊肉</td>
	</tr>
	<tr>
		<td rowspan=3>腌肉</td>
		<td>腊肉</td>
	</tr>
	<tr>
		<td>午餐肉</td>
	</tr>
	<tr>
		<td>叉烧</td>
	</tr>
	<tr>
		<td rowspan=6>肉肠</td>
		<td>香肠</td>
	</tr>
	<tr>
		<td>腊肠</td>
	</tr>
	<tr>
		<td>烤肠</td>
	</tr>
	<tr>
		<td>肉肠</td>
	</tr>
	<tr>
		<td>红肠</td>
	</tr>
	<tr>
		<td>热狗</td>
	</tr>
	<tr>
		<td rowspan=2>火腿</td>
		<td>火腿</td>
	</tr>
	<tr>
		<td>熟火腿</td>
	</tr>
	<tr>
		<td>肉松</td>
		<td>肉松</td>
	</tr>
	<tr>
		<td>脆骨</td>
		<td>脆骨</td>
	</tr>
	<tr>
		<td>小龙虾</td>
		<td>小龙虾</td>
	</tr>
	<tr>
		<td>鸡蛋</td>
		<td>鸡蛋</td>
	</tr>
	<tr>
		<td rowspan=16>水果类</td>
		<td>菠萝</td>
		<td>菠萝</td>
	</tr>
	<tr>
		<td>凤梨</td>
		<td>凤梨</td>
	</tr>
	<tr>
		<td rowspan=3>榴莲</td>
		<td>榴莲</td>
	</tr>
	<tr>
		<td>榴梿</td>
	</tr>
	<tr>
		<td>榴莲果</td>
	</tr>
	<tr>
		<td>樱桃</td>
		<td>樱桃</td>
	</tr>
	<tr>
		<td>黄桃</td>
		<td>黄桃</td>
	</tr>
	<tr>
		<td>柠檬</td>
		<td>柠檬</td>
	</tr>
	<tr>
		<td>香蕉</td>
		<td>香蕉</td>
	</tr>
	<tr>
		<td>芒果</td>
		<td>芒果</td>
	</tr>
	<tr>
		<td rowspan=3>椰子</td>
		<td>椰果</td>
	</tr>
	<tr>
		<td>椰蓉</td>
	</tr>
	<tr>
		<td>清椰</td>
	</tr>
	<tr>
		<td>火龙果</td>
		<td>火龙果</td>
	</tr>
	<tr>
		<td>苹果</td>
		<td>苹果</td>
	</tr>
	<tr>
		<td>蔓越莓</td>
		<td>蔓越莓</td>
	</tr>
	<tr>
		<td rowspan=18>海鲜水产类</td>
		<td>鱿鱼</td>
		<td>鱿鱼</td>
	</tr>
	<tr>
		<td>章鱼</td>
		<td>章鱼</td>
	</tr>
	<tr>
		<td rowspan=2>墨鱼</td>
		<td>墨鱼</td>
	</tr>
	<tr>
		<td>乌贼</td>
	</tr>
	<tr>
		<td rowspan=6>虾类</td>
		<td>虾</td>
	</tr>
	<tr>
		<td>虾仁</td>
	</tr>
	<tr>
		<td>大虾</td>
	</tr>
	<tr>
		<td>鲜虾</td>
	</tr>
	<tr>
		<td>虾球</td>
	</tr>
	<tr>
		<td>虾肉</td>
	</tr>
	<tr>
		<td>金枪鱼</td>
		<td>金枪鱼</td>
	</tr>
	<tr>
		<td>三文鱼</td>
		<td>三文鱼</td>
	</tr>
	<tr>
		<td>吞拿鱼</td>
		<td>吞拿鱼</td>
	</tr>
	<tr>
		<td>鳗鱼</td>
		<td>鳗鱼</td>
	</tr>
	<tr>
		<td>银鱼</td>
		<td>银鱼</td>
	</tr>
	<tr>
		<td>扇贝</td>
		<td>扇贝</td>
	</tr>
	<tr>
		<td>蟹类</td>
		<td>蟹肉</td>
	</tr>
	<tr>
		<td>海苔</td>
		<td>海苔</td>
	</tr>
	<tr>
		<td rowspan=37>辅料佐料</td>
		<td rowspan=2>奶油</td>
		<td>奶油</td>
	</tr>
	<tr>
		<td>白汁</td>
	</tr>
	<tr>
		<td>奶酪</td>
		<td>奶酪</td>
	</tr>
	<tr>
		<td>乳酪</td>
		<td>乳酪</td>
	</tr>
	<tr>
		<td>起士</td>
		<td>起士</td>
	</tr>
	<tr>
		<td>小米</td>
		<td>小米</td>
	</tr>
	<tr>
		<td>番茄酱</td>
		<td>番茄酱</td>
	</tr>
	<tr>
		<td>蛋黄酱</td>
		<td>蛋黄酱</td>
	</tr>
	<tr>
		<td>奶盖酱</td>
		<td>奶盖酱</td>
	</tr>
	<tr>
		<td rowspan=2>千岛酱</td>
		<td>千岛</td>
	</tr>
	<tr>
		<td>千岛酱</td>
	</tr>
	<tr>
		<td>沙拉酱</td>
		<td>沙拉酱</td>
	</tr>
	<tr>
		<td>果酱</td>
		<td>果酱</td>
	</tr>
	<tr>
		<td>辣酱</td>
		<td>辣酱</td>
	</tr>
	<tr>
		<td>蜂蜜</td>
		<td>蜂蜜</td>
	</tr>
	<tr>
		<td>芥末</td>
		<td>芥末</td>
	</tr>
	<tr>
		<td rowspan=2>黑胡椒</td>
		<td>黑椒</td>
	</tr>
	<tr>
		<td>黑胡椒</td>
	</tr>
	<tr>
		<td>花椒</td>
		<td>花椒</td>
	</tr>
	<tr>
		<td>迷迭香</td>
		<td>迷迭香</td>
	</tr>
	<tr>
		<td>茴香</td>
		<td>茴香</td>
	</tr>
	<tr>
		<td>芝麻</td>
		<td>芝麻</td>
	</tr>
	<tr>
		<td>香草</td>
		<td>香草</td>
	</tr>
	<tr>
		<td rowspan=2>大蒜</td>
		<td>大蒜</td>
	</tr>
	<tr>
		<td>蒜蓉</td>
	</tr>
	<tr>
		<td>咖喱</td>
		<td>咖喱</td>
	</tr>
	<tr>
		<td>薄荷</td>
		<td>薄荷</td>
	</tr>
	<tr>
		<td>慕斯</td>
		<td>慕斯</td>
	</tr>
	<tr>
		<td>酸奶</td>
		<td>酸奶</td>
	</tr>
	<tr>
		<td>土豆泥</td>
		<td>土豆泥</td>
	</tr>
	<tr>
		<td>桃仁</td>
		<td>桃仁</td>
	</tr>
	<tr>
		<td>板栗</td>
		<td>板栗</td>
	</tr>
	<tr>
		<td>焦糖</td>
		<td>焦糖</td>
	</tr>
	<tr>
		<td>松露</td>
		<td>松露</td>
	</tr>
	<tr>
		<td>三文治</td>
		<td>三文治</td>
	</tr>
	<tr>
		<td>橄榄油</td>
		<td>橄榄油</td>
	</tr>
	<tr>
		<td>黄油</td>
		<td>黄油</td>
	</tr>
  </table>

- 特征与标签提取  
  根据上述表格的分类，可以得到130个子类，这些就是我们需要提取的特征了。参考词袋模型表达文本信息，我们也给每个披萨商品构建一个1*130的向量，每个特征占据一个维度，如果该商品包含该特征，则该维度的值为1，否则该维度值为0，这样得到了每个披萨商品的特征向量  
  我们想要预测披萨商品畅销与否，有了特征之后还需要提取披萨商品的标签。观察数据发现，我们可以通过判断商品评星是否大于店铺口味评星来判断，如果某件商品评星高于店铺口味评星，则说明该商品畅销，标记为1，否则标记为0  
  ```
  def rate_to_marker(food_score, item_rating):
      if item_rating >= food_score:
          return np.array([[1]])
      else:
          return np.array([[0]])
  ```  
- 神经网络模型  
  本项目实现的神经网络共有4层，第一层共有64个神经元，且包含0.8的droupout，第二层共有16个神经元，第三层共有8层神经元，最后一层是输出层，所有层的激活函数都是sigmoid函数，本项目使用kears库实现模型  
  ```
  model = Sequential()
  model.add(Dense(64, activation='sigmoid', input_dim=X.shape[1]))
  model.add(Dropout(0.8))
  model.add(Dense(16, activation='sigmoid'))
  model.add(Dense(8, activation='sigmoid'))
  model.add(Dense(1, activation='sigmoid'))
  ```  
  模型的一些参数是包括：
  
  参数 | 值  |:-|:-|
  优化函数 | 梯度下降SGD
  损失函数 | 均方误差mse  
  学习率 | 0.001
  batch | 32
  epoch | 100
  交叉验证比例 | 0.2
  
  将模型训练中的loss和accuracy绘制成plot展示，可以看到最后训练集和验证集的accuracy都达到了80%以上，且最终趋于稳定，没有产生过拟合现象  
  ![nn_plot](http://oswrmk9hd.bkt.clouddn.com/nn_plot)  
  最后使用测试集测试模型的泛化能力，发现准确率可以达到0.811，与训练样本的准确率0.815相近，证明整个模型的能力还是不错的
- XGBoost
  本项目还实用XGBoost实现了预测模型，具体参数如下
  
  参数 | 值  |:-|:-|
  booster | gbtree
  max_depth | 18 
  scale_pos_weight | 0.8
  eta | 0.5
  epoch | 100
  objective | binary:logistic
  eval_metric | ['error', 'auc']
  迭代次数 | 500
  交叉验证比例 | 0.2
  
  由于XGBoost的评价函数中没有precision，本项目结合sklearn自定义了评价函数，应用于每个round中  
  ```
  def precision_and_recall(preds, dtrain):
      lab = dtrain.get_label()
      preds = [int(i >= 0.5) for i in preds]
      conf = confusion_matrix(lab, preds)
  	  precision = float(conf[0][0]) / float(conf[1][0]+conf[0][0])
      recall = float(conf[0][0]) / float(conf[0][1]+conf[0][0])
      return 'precision', precision
  ```  
  模型的训练过程可视化的结果如下图  
  ![xgboost](http://oswrmk9hd.bkt.clouddn.com/xgboost_plot)  
  可以看到训练集验证集的精度最终都可以达到0.8以上，但验证集error下降的不是很明显，但这个是效果较好的一组参数了，后期还需要对模型参数多摸索！  
  最后用测试集数据对模型进行验证，测试集精度达到0.826，可以看出整个模型的效果还是不错的  
  XGBoost通过训练最后可以得到一个特征的重要性评分，我们最后看到重要性排名前20的特征是
  
  排名 | 特征
  |:-|:-|
  1 | 洋葱
  2 | 菜椒 
  3 | 菌菇
  4 | 菠萝
  5 | 培根
  6 | 牛肉
  7 | 火腿
  8 | 鸡肉
  9 | 肉肠
  10 | 玉米
  11 | 番茄
  12 | 榴莲
  13 | 意式风味
  14 | 奶酪
  15 | 奥尔良风味
  16 | 烤制
  17 | 热带风味
  18 | 土豆
  19 | 薄底
  20 | 虾类
  
  分析可以看出，蔬菜类、水果类和荤菜类还是对销量有很大的影响，烹制方法和配料的影响并不是很大。
  随机森林也可以输出特征重要性指标  
  ```
  rf = RandomForestClassifier()
  rf.fit(X, y)
  names = ["X%s" % x for x in range(0, 130)]
  print "Features sorted by their score:"
  print sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), reverse=True)
  ```  
  随机森林输出的重要性排名前20的特征是
  
  排名 | 特征
  |:-|:-|
  1 | 鸡肉
  2 | 洋葱   
  3 | 菜椒
  4 | 菌菇
  5 | 培根
  6 | 牛肉
  7 | 玉米
  8 | 肉肠
  9 | 奶酪
  10 | 烤制
  11 | 火腿
  12 | 意式风味
  13 | 菠萝
  14 | 番茄
  15 | 番茄酱
  16 | 香
  17 | 薄底
  18 | 奥尔良风味
  19 | 橄榄
  20 | 热带风味
  
  对比XGBoost输出的特征重要性结果，两份结果在前20的特征有17个是相同的，洋葱、菜椒、菌菇、鸡肉、培根等特征在两个模型中重要性都非常高，这便是我们想要得到的结果了，这些特征对于销量起到了关键性的作用。同时，可以看到意式风味、奥尔良风味和热带风味是最受欢迎的3个口味，鸡肉牛肉也是比较畅销的品类......
## 展望
- 本项目披萨品类的特征仅仅只包含商品描述的语义信息，未来可以探索一些其它重要特征来描述披萨商品，使数据表达更加完整精确
- XGBoost验证集进度提升较为困难，调参是一门“玄学”，考虑通过网格搜索再优化一下参数的配置，争取达到更好的效果  
## 和我联系
E-mail: 535848615@qq.com  
GitHub主页: [https://github.com/JohnsonKlose](https://github.com/JohnsonKlose)  
博客园: [http://www.cnblogs.com/KloseJiao/](http://www.cnblogs.com/KloseJiao/)  
喜欢的朋友们可以加个star，也欢迎留言和邮件与我交流！