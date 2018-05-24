import pandas as pd

data = pd.read_csv('./result/fuzimiao.csv')
data = data.append(pd.read_csv('./result/gulou.csv'))
data = data.append(pd.read_csv('./result/hongyuecheng.csv'))
data = data.append(pd.read_csv('./result/huanyucheng.csv'))
data = data.append(pd.read_csv('./result/jiqingmendajie.csv'))
data = data.append(pd.read_csv('./result/nanjingzhan.csv'))
data = data.append(pd.read_csv('./result/sanpailou.csv'))
data = data.append(pd.read_csv('./result/xianmen.csv'))
data = data.append(pd.read_csv('./result/xinjiekou.csv'))
data = data.append(pd.read_csv('./result/xianlin.csv'))
data = data.append(pd.read_csv('./result/jiangningqu.csv'))
data = data.append(pd.read_csv('./result/hanzhongmen.csv'))
data = data.append(pd.read_csv('./result/yaohuamen.csv'))
data = data.append(pd.read_csv('./result/youfangqiao.csv'))
data = data.append(pd.read_csv('./result/renmingguangchang_sh.csv'))
data = data.append(pd.read_csv('./result/xujiahui_sh.csv'))
data = data.append(pd.read_csv('./result/xintiandi_sh.csv'))
data = data.append(pd.read_csv('./result/shanghaizhan_sh.csv'))
data = data.append(pd.read_csv('./result/lujiazui_sh.csv'))
data = data.append(pd.read_csv('./result/zhangjianggaoke_sh.csv'))
data = data.append(pd.read_csv('./result/putuoqu_sh.csv'))
data = data.append(pd.read_csv('./result/luwanqu_sh.csv'))
data = data.append(pd.read_csv('./result/jinganqu_sh.csv'))
data = data.append(pd.read_csv('./result/waitan_sh.csv'))
data = data.append(pd.read_csv('./result/wujiaochang_sh.csv'))
data = data.append(pd.read_csv('./result/dapuqiao_sh.csv'))
data = data.append(pd.read_csv('./result/minhang_sh.csv'))
data = data.append(pd.read_csv('./result/shijigongyuan_sh.csv'))

data = data.drop_duplicates(['item_id'])
data = data[data['item_rating'] > 0]
# data = data[data['item_description'] != ' ']
# data_positive = data[data['shop_food_score'] <= data['item_rating']]
print data.describe()
print data[:14]


def return_data():
    return data

# print data[data['item_id'] == 1677700007]
# print data.groupby('item_id')['item_id'].count()
# print data_positive.describe()