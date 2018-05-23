# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


def word_to_label(cut_words):
    label = np.zeros((1, 130), dtype=np.int16)
    words = cut_words.split(",")

    if "夏威夷" in words or "热带" in words:
        # 热带风味
        label[0][0] = 1
    if "意式" in words or "意大利" in words or "那不勒斯" in words or "博洛尼亚" in words \
            or "西西里" in words or "贝贝罗尼" in words or "罗马" in words:
        # 意式风味
        label[0][1] = 1
    if "泰国" in words or "泰式" in words or "马来西亚" in words:
        # 东南亚风味
        label[0][2] = 1
    if "墨西哥" in words:
        # 墨西哥风味
        label[0][3] = 1
    if "奥尔良" in words or "新奥尔良" in words:
        # 奥尔良风味
        label[0][4] = 1
    if "澳洲" in words or "新西兰" in words:
        # 澳洲风味
        label[0][5] = 1
    if "法国" in words:
        # 法国风味
        label[0][6] = 1
    if "美国" in words or "纽约" in words:
        # 美式风味
        label[0][7] = 1
    if "荷兰" in words:
        # 荷兰风味
        label[0][8] = 1
    if "德式" in words or "德国" in words:
        # 德式风味
        label[0][9] = 1
    if "台湾" in words:
        # 台湾风味
        label[0][10] = 1
    if "韩国" in words or "韩式" in words:
        # 韩式风味
        label[0][11] = 1
    if "日式" in words:
        # 日式风味
        label[0][12] = 1
    if "京味" in words or "川香" in words:
        # 中式风味
        label[0][13] = 1
    if "海陆" in words:
        # 海陆风味
        label[0][14] = 1
    if "全素" in words:
        # 全素风味
        label[0][15] = 1

    if "香脆" in words or "脆爽" in words or "松脆" in words or "薄脆" in words or "酥脆" in words:
        # 脆
        label[0][16] = 1
    if "鲜美" in words or "香鲜" in words:
        # 鲜
        label[0][17] = 1
    if "酸甜" in words:
        # 酸
        label[0][18] = 1
    if "酸甜" in words or "香甜" in words or "甜辣" in words:
        # 甜
        label[0][19] = 1
    if "微辣" in words or "香辣" in words or "麻辣" in words or "辣爽" in words or "甜辣" in words:
        # 辣
        label[0][20] = 1
    if "香醇" in words or "醇香" in words or "醇厚" in words:
        # 醇
        label[0][21] = 1
    if "清甜" in words or "清新" in words or "清脆" in words:
        # 清
        label[0][22] = 1
    if "柔韧" in words or "柔嫩" in words:
        # 柔
        label[0][23] = 1
    if "果香" in words or "芝香" in words or "五香" in words or "香甜" in words or "香鲜" in words or "浓香" in words:
        # 香
        label[0][24] = 1

    if "薄底" in words or "薄饼" in words:
        # 薄底
        label[0][25] = 1
    if "厚底" in words:
        # 厚底
        label[0][26] = 1
    if "铁盘" in words:
        # 铁盘
        label[0][27] = 1
    if "烘烤" in words or "烤" in words or "BBQ" in words or "烤制" in words or "烧烤" in words \
            or "现烤" in words or "烤肉" in words:
        # 烤制
        label[0][28] = 1
    if "岩烧" in words:
        # 岩烧
        label[0][29] = 1
    if "炭烧" in words:
        # 炭烧
        label[0][30] = 1
    if "腌制" in words:
        # 腌制
        label[0][31] = 1
    if "焗" in words:
        # 焗烧
        label[0][32] = 1
    if "蜜汁" in words:
        # 蜜汁
        label[0][33] = 1

    if "彩椒" in words or "青椒" in words or "红椒" in words or "红彩椒" in words \
            or "黄彩椒" in words or "灯笼椒" in words or "甜椒" in words:
        # 菜椒
        label[0][34] = 1
    if "脆椒" in words or "辣椒" in words or "尖椒" in words:
        # 辣椒
        label[0][35] = 1
    if "橄榄" in words:
        # 橄榄
        label[0][36] = 1
    if "洋葱" in words or "onion" in words or "onions" in words:
        # 洋葱
        label[0][37] = 1
    if "京葱" in words:
        # 京葱
        label[0][38] = 1
    if "青葱" in words:
        # 青葱
        label[0][39] = 1
    if "玉米" in words or "玉米片" in words or "玉米粒" in words:
        # 玉米
        label[0][40] = 1
    if "荞麦" in words or "荞麦面" in words:
        # 荞麦
        label[0][41] = 1
    if "黄瓜" in words or "酸黄瓜" in words:
        # 黄瓜
        label[0][42] = 1
    if "西红柿" in words or "番茄" in words or "蕃茄" in words:
        # 番茄
        label[0][43] = 1
    if "蘑菇" in words or "松露菌" in words or "褐菇" in words:
        # 菌菇
        label[0][44] = 1
    if "青豆" in words:
        # 青豆
        label[0][45] = 1
    if "芦笋" in words:
        # 芦笋
        label[0][46] = 1
    if "莴笋" in words:
        # 莴笋
        label[0][47] = 1
    if "西葫芦" in words:
        # 西葫芦
        label[0][48] = 1
    if "南瓜" in words:
        # 南瓜
        label[0][49] = 1
    if "香菜" in words:
        # 香菜
        label[0][50] = 1
    if "菠菜" in words:
        # 菠菜
        label[0][51] = 1
    if "西兰花" in words:
        # 西兰花
        label[0][52] = 1
    if "藕" in words or "藕片" in words:
        # 藕
        label[0][53] = 1
    if "茄子" in words:
        # 茄子
        label[0][54] = 1
    if "土豆" in words or "土豆片" in words or "薯角" in words or "薯条" in words or "脆薯" in words:
        # 土豆
        label[0][55] = 1
    if "红薯" in words:
        # 红薯
        label[0][56] = 1

    if "培根" in words:
        # 培根
        label[0][57] = 1
    if "牛肉" in words or "牛排" in words:
        # 牛肉
        label[0][58] = 1
    if "鸡肉" in words or "烤鸡" in words or "鸡腿肉" in words or "鸡胸" in words or "鸡胸肉" in words or "鸡丁" in words:
        # 鸡肉
        label[0][59] = 1
    if "猪肉" in words or "里脊" in words:
        # 猪肉
        label[0][60] = 1
    if "鸭肉" in words:
        # 鸭肉
        label[0][61] = 1
    if "北京烤鸭" in words or "烤鸭" in words:
        # 烤鸭
        label[0][62] = 1
    if "羊肉" in words:
        # 羊肉
        label[0][63] = 1
    if "腊肉" in words or "午餐肉" in words or "叉烧" in words:
        # 腌肉
        label[0][64] = 1
    if "香肠" in words or "腊肠" in words or "烤肠" in words or "肉肠" in words or "红肠" in words or "热狗" in words:
        # 肉肠
        label[0][65] = 1
    if "火腿" in words or "熟火腿" in words:
        # 火腿
        label[0][66] = 1
    if "肉松" in words:
        # 肉松
        label[0][67] = 1
    if "脆骨" in words:
        # 脆骨
        label[0][68] = 1
    if "小龙虾" in words:
        # 小龙虾
        label[0][69] = 1
    if "鸡蛋" in words:
        # 鸡蛋
        label[0][70] = 1

    if "菠萝" in words:
        # 菠萝
        label[0][71] = 1
    if "凤梨" in words:
        # 凤梨
        label[0][72] = 1
    if "榴莲" in words or "榴梿" in words or "榴莲果" in words:
        # 榴莲
        label[0][73] = 1
    if "樱桃" in words:
        # 樱桃
        label[0][74] = 1
    if "黄桃" in words:
        # 黄桃
        label[0][75] = 1
    if "柠檬" in words:
        # 柠檬
        label[0][76] = 1
    if "香蕉" in words:
        # 香蕉
        label[0][77] = 1
    if "芒果" in words:
        # 芒果
        label[0][78] = 1
    if "椰果" in words or "椰蓉" in words or "清椰" in words:
        # 椰子
        label[0][79] = 1
    if "火龙果" in words:
        # 火龙果
        label[0][80] = 1
    if "木瓜" in words:
        # 木瓜
        label[0][81] = 1
    if "牛油果" in words:
        # 牛油果
        label[0][82] = 1
    if "苹果" in words:
        # 苹果
        label[0][83] = 1
    if "蔓越莓" in words:
        # 蔓越莓
        label[0][84] = 1

    if "鱿鱼" in words:
        # 鱿鱼
        label[0][85] = 1
    if "章鱼" in words:
        # 章鱼
        label[0][86] = 1
    if "墨鱼" in words or "乌贼" in words:
        # 墨鱼
        label[0][87] = 1
    if "虾" in words or "虾仁" in words or "大虾" in words or "鲜虾" in words or "虾球" in words or "虾肉" in words:
        # 虾类
        label[0][88] = 1
    if "金枪鱼" in words:
        # 金枪鱼
        label[0][89] = 1
    if "三文鱼" in words:
        # 三文鱼
        label[0][90] = 1
    if "吞拿鱼" in words:
        # 吞拿鱼
        label[0][91] = 1
    if "鳗鱼" in words:
        # 鳗鱼
        label[0][92] = 1
    if "银鱼" in words:
        # 银鱼
        label[0][93] = 1
    if "扇贝" in words:
        # 扇贝
        label[0][94] = 1
    if "蟹肉" in words:
        # 蟹类
        label[0][95] = 1
    if "海苔" in words:
        # 海苔
        label[0][96] = 1

    if "奶油" in words or "白汁" in words:
        # 奶油
        label[0][97] = 1
    if "奶酪" in words:
        # 奶酪
        label[0][98] = 1
    if "乳酪" in words:
        # 乳酪
        label[0][99] = 1
    if "起士" in words:
        # 起士
        label[0][100] = 1
    if "小米" in words:
        # 小米
        label[0][101] = 1
    if "番茄酱" in words:
        # 番茄酱
        label[0][102] = 1
    if "蛋黄酱" in words:
        # 蛋黄酱
        label[0][103] = 1
    if "奶盖酱" in words:
        # 奶盖酱
        label[0][104] = 1
    if "千岛酱" in words or " 千岛" in words:
        # 千岛酱
        label[0][105] = 1
    if "沙拉酱" in words:
        # 沙拉酱
        label[0][106] = 1
    if "果酱" in words:
        # 果酱
        label[0][107] = 1
    if "辣酱" in words:
        # 辣酱
        label[0][108] = 1
    if "蜂蜜" in words:
        # 蜂蜜
        label[0][109] = 1
    if "芥末" in words:
        # 芥末
        label[0][110] = 1
    if "黑椒" in words or "黑胡椒" in words:
        # 黑胡椒
        label[0][111] = 1
    if "花椒" in words:
        # 花椒
        label[0][112] = 1
    if "迷迭香" in words:
        # 迷迭香
        label[0][113] = 1
    if "茴香" in words:
        # 茴香
        label[0][114] = 1
    if "芝麻" in words:
        # 芝麻
        label[0][115] = 1
    if "香草" in words:
        # 香草
        label[0][116] = 1
    if "大蒜" in words or "蒜蓉" in words:
        # 大蒜
        label[0][117] = 1
    if "咖喱" in words:
        # 咖喱
        label[0][118] = 1
    if "薄荷" in words:
        # 薄荷
        label[0][119] = 1
    if "慕斯" in words:
        # 慕斯
        label[0][120] = 1
    if "酸奶" in words:
        # 酸奶
        label[0][121] = 1
    if "土豆泥" in words:
        # 土豆泥
        label[0][122] = 1
    if "桃仁" in words:
        # 桃仁
        label[0][123] = 1
    if "板栗" in words:
        # 板栗
        label[0][124] = 1
    if "焦糖" in words:
        # 焦糖
        label[0][125] = 1
    if "松露" in words:
        # 松露
        label[0][126] = 1
    if "三文治" in words:
        # 三文治
        label[0][127] = 1
    if "橄榄油" in words:
        # 橄榄油
        label[0][128] = 1
    if "黄油" in words:
        # 黄油
        label[0][129] = 1

    return label


def rate_to_marker(food_score, item_rating):
    if item_rating >= food_score:
        return np.array([[1]])
    else:
        return np.array([[0]])


def make_labels(cut_column, food_score_column, item_rating_column):
    labels_np = None
    marker_np = None
    for i in range(cut_column.shape[0]):
        row = cut_column.iloc[i]
        print row
        if i == 0:
            labels_np = word_to_label(row)
            marker_np = rate_to_marker(food_score_column.iloc[i], item_rating_column.iloc[i])
        else:
            row_label = word_to_label(row)
            if 1 in row_label:
                labels_np = np.concatenate((labels_np, word_to_label(row)))
                marker_np = np.concatenate((marker_np, rate_to_marker(food_score_column.iloc[i],
                                                                      item_rating_column.iloc[i])))
            else:
                continue

    return labels_np, marker_np


if __name__ == "__main__":
    st = "比萨, 酱, 芝士, 玉米, 火腿, 鸡肉, 培根, 菠萝, 柠檬, 奶油, 酱,, 车达, 芝士, 干法, 香"
    if "夏威夷" in st or "热带" in st:
        # 热带风味
        print "热带风味"
    # t = np.zeros(20)
    # print t
    # t[0] = 1
    # print t
    # words = ["我", "是", "学生"]
    # if "我" in words:
    #     print "success"