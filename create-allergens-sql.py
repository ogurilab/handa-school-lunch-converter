import json


def generate_insert_sql(dishes_json_path, allergens_json_path, allergens_map):
    with open(dishes_json_path, "r", encoding="utf-8") as file:
        dishes_data = json.load(file)

    with open(allergens_json_path, "r", encoding="utf-8") as file:
        allergens_data = json.load(file)

    # すでに処理された組み合わせを記録するマップ
    processed_combinations = set()

    # SQLインサートコマンドを生成する
    values_list = []

    for dish in dishes_data:
        dish_id = dish["id"]
        dish_name = dish["name"]

        for allergen in allergens_data:
            if allergen["name"] == dish_name:
                for item in allergen["allergens"]:
                    allergen_name = item["name"]
                    category = item["type"]
                    allergen_id = allergens_map.get(allergen_name)

                    if allergen_id is not None:
                        # この組み合わせがすでに処理されたかチェック
                        combination_key = (allergen_id, dish_id, category)
                        if combination_key not in processed_combinations:
                            # 処理されていなければSQLコマンドに追加し、組み合わせを記録
                            values_list.append(
                                f"({allergen_id}, '{dish_id}', {category})"
                            )
                            processed_combinations.add(combination_key)

    insert_sql = f"INSERT INTO dishes_allergens (allergen_id, dish_id, category) VALUES {','.join(values_list)};"
    return insert_sql


# パスとアレルギーのマッピング辞書を定義
dishes_json_path = "./data/export/dishes.json"
allergens_json_path = "./data/concat/allergens/allergen-concat.json"
result_sql_path = "./data/sql/allergens/dishes_allergens.sql"
allergens_map = {
    "小麦": 1,
    "そば": 2,
    "卵": 3,
    "乳": 4,
    "落花生": 5,
    "あわび": 6,
    "いか": 7,
    "いくら": 8,
    "えび": 9,
    "オレンジ": 10,
    "かに": 11,
    "キウイフルーツ": 12,
    "牛肉": 13,
    "くるみ": 14,
    "さけ": 15,
    "さば": 16,
    "大豆": 17,
    "鶏肉": 18,
    "豚肉": 19,
    "まつたけ": 20,
    "もも": 21,
    "やまいも": 22,
    "りんご": 23,
    "ゼラチン": 24,
    "バナナ": 25,
    "ごま": 26,
    "カシューナッツ": 27,
    "アーモンド": 28,
}

# 関数を呼び出して単一のINSERT SQLコマンドを生成
insert_sql = generate_insert_sql(dishes_json_path, allergens_json_path, allergens_map)

with open(result_sql_path, "w", encoding="utf-8") as file:
    file.write(insert_sql)
