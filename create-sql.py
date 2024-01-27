import json
from datetime import datetime
import ulid

# JSONデータを読み込むためのパス
input_path = "./data/concat/concat.json"

# SQL文を保存するためのパス
output_path_menus = "./data/sql/menus.sql"
output_path_dishes = "./data/sql/dishes.sql"

# JSONデータを読み込む
with open(input_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# SQL文のためのリストを作成
menus_sql = []
dishes_sql = []

for entry in data:
    menu_id = str(ulid.new())  # ULIDを生成
    offered_at = entry["offered_at"]
    photo_url = f"https://storage.handa.city/{offered_at.replace('-', '')}.jpg"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # menusテーブル用のデータ
    menus_sql.append(
        f"INSERT INTO menus (id, offered_at, photo_url, created_at, elementary_school_calories, junior_high_school_calories, city_code) VALUES ('{menu_id}', '{offered_at}', '{photo_url}', '{created_at}', {entry['calories_elementary']}, {entry['calories_junior_high']}, 1);"
    )

    # dishesテーブル用のデータ
    for dish in entry["menu_items"]:
        dish_id = str(ulid.new())  # ULIDを生成
        # ON DUPLICATE KEY UPDATE 句を使用
        dishes_sql.append(
            f"INSERT INTO dishes (id, menu_id, name, created_at) VALUES ('{dish_id}', '{menu_id}', '{dish}', '{created_at}') ON DUPLICATE KEY UPDATE id=id;"
        )

# SQL文をファイルに保存

# menusテーブル用のSQL文
with open(output_path_menus, "w", encoding="utf-8") as file:
    file.write("\n".join(menus_sql))

# dishesテーブル用のSQL文
with open(output_path_dishes, "w", encoding="utf-8") as file:
    file.write("\n".join(dishes_sql))
