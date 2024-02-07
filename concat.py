import os
import json

# JSONファイルがあるディレクトリを指定
input_directory = "./data/output/menus/"  # 入力ファイルがあるディレクトリ
output_directory = "./data/concat/menus/"  # 結合されたファイルを保存するディレクトリ
output_file = "menu-concat.json"  # 出力ファイルの名前

# 全てのJSONデータを格納するリスト
all_data = []

# ディレクトリ内のすべてのファイルをループ処理
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):  # JSONファイルのみ処理
        filepath = os.path.join(input_directory, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            all_data.extend(data)  # リストにデータを追加

# 結合されたデータを新しいJSONファイルに書き出す
output_path = os.path.join(output_directory, output_file)
os.makedirs(output_directory, exist_ok=True)  # 出力ディレクトリがない場合は作成

with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(all_data, outfile, ensure_ascii=False, indent=4)
