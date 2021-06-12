from pyflink.table import EnvironmentSettings, TableEnvironment
import pandas as pd
from utils import genre, top_50_albums, album_sales, year_albums_and_tracks, top_5_genres_list, \
    top_5_genres_years_sales, top_5_genres_avg_scores, analysis_top_50_albums

if __name__ == "__main__":
    # 1. 设置用于批处理的初始环境属性
    settings = EnvironmentSettings.new_instance().in_batch_mode().use_blink_planner().build()
    t_env = TableEnvironment.create(settings)
    # 设置处理数据的并行度
    t_env.get_config().get_configuration().set_string("parallelism.default", "1")
    # 设置读入数据的路径
    data_dir = '/home2/zgx/data/Albums_data/'
    # 设置保存json文件的路径
    json_save_dir = '/home2/zgx/codes/Flink_Music_Albums_Data_Analysis/static/data/'
    # 2. 读入csv文件转为pandas的DataFrame对象
    pdf = pd.read_csv(data_dir + 'albums.csv')
    # 3. 将DataFrame对象转化为Flink的Table的对象
    table = t_env.from_pandas(pdf)
    # 4. 第一个数据分析图像：统计20年间各类风格的音乐专辑的总数量，并保存在genre.json中
    genre(table, json_save_dir, 'genre.json')
    # 5. 第二个数据分析图像：统计20年间销量在前50的音乐专辑名称，数据保存在top_50_albums.json中并用词云显示
    top_50_albums(table, json_save_dir, 'top_50_albums.json')
    analysis_top_50_albums()
    # 6. 第三个数据分析图像：统计20年间各类型专辑的销量统计图，数据保存在album_sales.json中
    album_sales(table, json_save_dir, album_sales.json)
    # 7. 第四个数据分析图像，统计20年间每年发行的专辑数量和单曲数量,数据保存在year_albums_and_tracks.json中
    year_albums_and_tracks(table, json_save_dir, 'year_albums_and_tracks.json')
    # 8. 第五个数据分析图像：统计20年间总销量前五的专辑类型的各年份销量，数据保存在top_5_genres_year_sales.json中
    top_5_genres_years_sales(table, top_5_genres_list(table), json_save_dir, 'top_5_genres_year_sales.json')
    # 9. 第六个数据分析图像：统计20年间总销量前五的专辑类型在不同评分系统上的分数，数据保存在top_5_genres_avg_scores.json中
    top_5_genres_avg_scores(table, top_5_genres_list(table), json_save_dir, 'top_5_genres_avg_scores.json')
