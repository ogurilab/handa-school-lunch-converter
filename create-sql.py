from datetime import datetime
import ulid
import json

# JSONデータを読み込むためのパス
input_path = "./data/concat/menus/menu-concat.json"

# SQL文を保存するためのパス
output_path = "./data/sql/menus/handashi.sql"

# JSONデータを読み込む
with open(input_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# SQL文のためのリストを作成
menus_values = []
dishes_values = []
menu_dishes_values = []

# dishesのnameとidのマッピング
dishes_name_id_mapping = {}

for entry in data:
    menu_id = str(ulid.new())
    offered_at = entry["offered_at"]
    photo_url = f"https://storage.handa.city/{offered_at.replace('-', '')}.jpg"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Noneの場合は0を使用
    elementary_calories = (
        entry["calories_elementary"] if entry["calories_elementary"] else 0
    )
    junior_high_calories = (
        entry["calories_junior_high"] if entry["calories_junior_high"] else 0
    )

    # menusテーブル用の値
    menus_values.append(
        f"('{menu_id}', '{offered_at}', '{photo_url}', '{created_at}', {elementary_calories}, {junior_high_calories}, 23205)"
    )

    # dishesテーブルおよびmenu_dishesテーブル用のデータ
    for dish in entry["menu_items"]:
        if dish not in dishes_name_id_mapping:
            dish_id = str(ulid.new())
            dishes_values.append(f"('{dish_id}', '{dish}', '{created_at}')")
            dishes_name_id_mapping[dish] = dish_id
        else:
            dish_id = dishes_name_id_mapping[dish]

        # menu_dishesテーブル用の値
        menu_dishes_values.append(f"('{menu_id}', '{dish_id}')")

# SQL文を生成
menus_sql = f"INSERT INTO menus (id, offered_at, photo_url, created_at, elementary_school_calories, junior_high_school_calories, city_code) VALUES {','.join(menus_values)};"
dishes_sql = f"INSERT INTO dishes (id, name, created_at) VALUES {','.join(dishes_values)} ON DUPLICATE KEY UPDATE id=id;"
menu_dishes_sql = (
    f"INSERT INTO menu_dishes (menu_id, dish_id) VALUES {','.join(menu_dishes_values)};"
)

# SQL文をファイルに保存
with open(output_path, "w", encoding="utf-8") as file:
    file.write(menus_sql + "\n\n" + dishes_sql + "\n\n" + menu_dishes_sql)
