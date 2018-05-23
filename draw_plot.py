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