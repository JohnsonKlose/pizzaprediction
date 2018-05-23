import pandas as pd

data = pd.read_csv('fuzimiao.csv')
data = data.append(pd.read_csv('gulou.csv'))
data = data.append(pd.read_csv('hongyuecheng.csv'))
data = data.append(pd.read_csv('huanyucheng.csv'))
data = data.append(pd.read_csv('jiqingmendajie.csv'))
data = data.append(pd.read_csv('nanjingzhan.csv'))
data = data.append(pd.read_csv('sanpailou.csv'))
data = data.append(pd.read_csv('xianmen.csv'))
data = data.append(pd.read_csv('xinjiekou.csv'))
data = data.append(pd.read_csv('xianlin.csv'))
data = data.append(pd.read_csv('jiangningqu.csv'))
data = data.append(pd.read_csv('hanzhongmen.csv'))
data = data.append(pd.read_csv('yaohuamen.csv'))
data = data.append(pd.read_csv('youfangqiao.csv'))
data = data.append(pd.read_csv('renmingguangchang_sh.csv'))
data = data.append(pd.read_csv('xujiahui_sh.csv'))
data = data.append(pd.read_csv('xintiandi_sh.csv'))
data = data.append(pd.read_csv('shanghaizhan_sh.csv'))
data = data.append(pd.read_csv('lujiazui_sh.csv'))
data = data.append(pd.read_csv('zhangjianggaoke_sh.csv'))
data = data.append(pd.read_csv('putuoqu_sh.csv'))
data = data.append(pd.read_csv('luwanqu_sh.csv'))
data = data.append(pd.read_csv('jinganqu_sh.csv'))
data = data.append(pd.read_csv('waitan_sh.csv'))
data = data.append(pd.read_csv('wujiaochang_sh.csv'))
data = data.append(pd.read_csv('dapuqiao_sh.csv'))
data = data.append(pd.read_csv('minhang_sh.csv'))
data = data.append(pd.read_csv('shijigongyuan_sh.csv'))

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