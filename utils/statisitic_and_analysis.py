from pyflink.table.expressions import lit, col
import json


# 第1个图：统计20年间各类风格的音乐专辑的总数量
def genre(table, json_save_dir, file_name):
    table_results = table.group_by(col("genre")).select(col("genre"), lit(1).count.alias("genre_num")).execute()
    # table_results.print()
    res = []
    with table_results.collect() as results:
        for result in results:
            res.append(result.__dict__.get('_values'))

    f = open(json_save_dir + file_name, 'w')
    f.write(json.dumps(res))
    f.close()


# 第2个图：统计20年间销量在前50的音乐专辑名称并用词云显示
def top_50_albums(table, json_save_dir, file_name):
    table_results = table.select(col("album_title"), col("num_of_sales")).order_by(
        col("num_of_sales").desc).limit(50).execute()
    ans = {}
    with table_results.collect() as results:
        for result in results:
            ans[result.__dict__.get('_values')[0]] = result.__dict__.get('_values')[1] - 999000

    f = open(json_save_dir + file_name, 'w')
    f.write(json.dumps(ans))
    f.close()


# 第3个图：各类型专辑的销量统计图
def album_sales(table, json_save_dir, file_name):
    table_results = table.group_by(col("genre")).select(col("genre"),
                                                        col("num_of_sales").sum.alias(
                                                            "each_album_genre_sales")).execute()

    # table_results.print()
    res = []
    with table_results.collect() as results:
        for result in results:
            res.append(result.__dict__.get('_values'))

    f = open(json_save_dir + file_name, 'w')

    f.write(json.dumps(res))
    f.close()


# 第4个图：统计每年的专辑数量和单曲数量
def year_albums_and_tracks(table, json_save_dir, file_name):
    table_results = table.group_by(col("year_of_pub")).select(col("year_of_pub"),
                                                              col("genre").count.alias("genres_num"),
                                                              col("num_of_tracks").sum.alias("tracks_num")).order_by(
        col("year_of_pub").asc).execute()

    # table_results.print()
    ans = {"tracks": [], "years": [], "albums": []}
    with table_results.collect() as results:
        for result in results:
            # res.append(result.__dict__.get('_values'))
            ans["tracks"].append(result.__dict__.get('_values')[2])
            ans["years"].append(result.__dict__.get('_values')[0])
            ans["albums"].append(result.__dict__.get('_values')[1])

    f = open(json_save_dir + file_name, 'w')
    f.write(json.dumps(ans))
    f.close()


# 返回总销量是前五的专辑类型
def top_5_genres_list(table):
    table_results = table.group_by(col("genre")).select(col("genre"),
                                                        col("num_of_sales").sum.alias("each_album_sales")).order_by(
        col("each_album_sales").desc).limit(5).execute()
    list = []
    with table_results.collect() as results:
        for result in results:
            # print(result.__dict__.get('_values')[0])
            list.append(result.__dict__.get('_values')[0])
    # print(list)
    return list


# 第五个图：总销量前五类型的专辑各年份销量
def top_5_genres_years_sales(table, genres_list, json_save_dir, file_name):
    ans = {}
    for genre in genres_list:
        table_results = table.filter(col("genre") == genre).group_by(col("year_of_pub")).select(col("year_of_pub"), col(
            "num_of_sales").sum.alias(
            "years_of_sales")).order_by(
            col("year_of_pub").asc).execute()
        list = []
        with table_results.collect() as results:
            for result in results:
                result.__dict__.get('_values').insert(0, genre)
                list.append(result.__dict__.get('_values'))
        ans[genre] = list

    f = open(json_save_dir + file_name, 'w')
    f.write(json.dumps(ans))
    f.close()


# 第六个图：总销量前五专辑类型在不同评分系统的平均分数
def top_5_genres_avg_scores(table, genres_list, json_save_dir, file_name):
    # genres_list = top_5_genres_list(table)
    list = []
    for genre in genres_list:
        table_results = table.filter(col("genre") == genre).select(col("rolling_stone_critic").avg,
                                                                   col("mtv_critic").avg,
                                                                   col("music_maniac_critic").avg).execute()
        with table_results.collect() as results:
            for result in results:
                temp = [round(x, 4) for x in result.__dict__.get('_values')]
                temp.insert(0, genre)
                list.append(temp)

    f = open(json_save_dir + file_name, 'w')
    f.write(json.dumps(list))
    f.close()
