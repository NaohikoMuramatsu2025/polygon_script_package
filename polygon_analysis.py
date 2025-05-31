import os
import csv
import configparser

# INIファイルの絶対パス取得と読み込み
ini_path = os.path.abspath('config.ini')
if not os.path.exists(ini_path):
    raise FileNotFoundError(f"config.ini が見つかりません: {ini_path}")

config = configparser.ConfigParser()
config.read(ini_path, encoding='utf-8')

# 設定取得
csv_file_name = config['INPUT']['csv_file']
csv_file_path = os.path.join(os.path.dirname(ini_path), csv_file_name)
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"CSV ファイルが見つかりません: {csv_file_path}")

x_col = config['FIELD']['x_column']
y_col = config['FIELD']['y_column']
print_result = config.getboolean('OUTPUT', 'print_result')

# CSVから座標データを読み込む関数
def load_vertices_from_csv(file_path, x_col, y_col):
    vertices = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                x = float(row[x_col])
                y = float(row[y_col])
                vertices.append((x, y))
            except KeyError as e:
                raise KeyError(f"列名が一致しません: {e}")
    return vertices

# N角形の面積と重心を計算する関数
def calculate_polygon_area_centroid(vertices):
    n = len(vertices)
    if n < 3:
        raise ValueError(f"頂点が {n} 点しかありません。ポリゴンとして成立しません。")

    area = 0.0
    centroid_x = 0.0
    centroid_y = 0.0

    for i in range(n):
        x_i, y_i = vertices[i]
        x_next, y_next = vertices[(i + 1) % n]
        cross_product = (x_i * y_next) - (x_next * y_i)
        area += cross_product
        centroid_x += (x_i + x_next) * cross_product
        centroid_y += (y_i + y_next) * cross_product

    area /= 2.0

    if abs(area) < 1e-10:
        raise ValueError("ポリゴンの面積がゼロです。一直線または重複点の可能性があります。")

    centroid_x /= (6.0 * area)
    centroid_y /= (6.0 * area)

    return abs(area), (centroid_x, centroid_y)

# メイン処理
try:
    vertices = load_vertices_from_csv(csv_file_path, x_col, y_col)
    area, centroid = calculate_polygon_area_centroid(vertices)

    if print_result:
        print(f"面積: {area}")
        print(f"重心: {centroid}")

except Exception as e:
    print(f"エラーが発生しました: {e}")
