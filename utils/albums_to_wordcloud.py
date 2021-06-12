from wordcloud import WordCloud
import json


def analysis_top_50_albums():
    data1 = json.load(open('../static/data/top_50_albums.json'))
    wc1 = WordCloud(background_color='white',
                    ).generate_from_frequencies(data1)

    wc1.to_file("../templates/word_cloud.jpg")
