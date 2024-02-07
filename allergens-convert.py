import pandas as pd
import json
import os
import traceback
import re  # 正規表現モジュールをインポート


def process_excel_file(file_path):
    df = pd.read_excel(file_path, header=9)
    defined_allergens = set(
        [
            "小麦",
            "そば",
            "卵",
            "乳",
            "落花生",
            "あわび",
            "いか",
            "いくら",
            "えび",
            "オレンジ",
            "かに",
            "キウイフルーツ",
            "牛肉",
            "くるみ",
            "さけ",
            "さば",
            "大豆",
            "鶏肉",
            "豚肉",
            "まつたけ",
            "もも",
            "やまいも",
            "りんご",
            "ゼラチン",
            "バナナ",
            "ごま",
            "カシューナッツ",
            "アーモンド",
        ]
    )

    # Excelファイルに存在するアレルギー情報の列をチェック
    existing_allergens = set()
    for column in df.columns:
        if any(column.startswith(allergen) for allergen in defined_allergens):
            existing_allergens.add(column)

    # 未定義のアレルギー情報列があればエラーを出力
    undefined_allergens = existing_allergens - defined_allergens
    if undefined_allergens:
        raise ValueError(f"未定義のアレルギー情報列が存在します: {undefined_allergens}")

    # データフレームのアレルギー情報列を数値型に変換
    for allergen_name in defined_allergens:
        if allergen_name in df.columns:
            df[allergen_name] = pd.to_numeric(
                df[allergen_name], errors="coerce"
            ).fillna(0)

    menu_allergens_list = []
    for _, row in df.iterrows():
        if "献立名" in df.columns:
            menu_name = row["献立名"]
            menu_name = re.sub(
                r"\（小学校のみ\）|\（中学校のみ\）", "", menu_name
            ).strip()

            allergens = []
            for allergen_name in defined_allergens:
                if allergen_name in existing_allergens and row[allergen_name] > 0:
                    allergens.append(
                        {"name": allergen_name, "type": int(row[allergen_name])}
                    )

            if allergens:
                menu_allergens_list.append({"name": menu_name, "allergens": allergens})

    return json.dumps(menu_allergens_list, ensure_ascii=False, indent=2)


def save_to_json(json_data, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(json_data)


def process_all_excel_files(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".xls"):
            file_path = os.path.join(input_directory, filename)
            try:
                json_data = process_excel_file(file_path)
                json_file_path = os.path.join(
                    output_directory, f"{os.path.splitext(filename)[0]}.json"
                )
                save_to_json(json_data, json_file_path)
            except Exception as e:
                error_msg = (
                    f"Error processing file {filename}: {e}\n{traceback.format_exc()}"
                )
                print(error_msg)


# 入力ディレクトリと出力ディレクトリのパスを指定
input_directory = "./data/input/allergens/"  # 適宜調整してください
output_directory = "./data/output/allergens/"  # 適宜調整してください

# 処理の実行
process_all_excel_files(input_directory, output_directory)
