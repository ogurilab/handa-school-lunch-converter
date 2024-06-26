import pandas as pd
import os
import traceback


# 特定のエクセルファイルを処理する関数
def process_excel_file(file_path):
    # データを処理してデータフレームを返す
    df = pd.read_excel(file_path, header=9)

    # 必要な列を確認して、存在しない場合は追加する
    columns_required = [
        "ic:年",
        "ic:月",
        "ic:日",
        "主食（パン・ごはん）",
        "献立名１",
        "献立名２",
        "献立名３",
        "献立名４",
        "献立名５",
        "献立名６",
        "飲み物",
        "カロリー（小学校）",
        "カロリー（中学校）",
    ]
    for column in ["献立名５", "献立名６"]:
        if column not in df.columns:
            df[column] = ""  # 存在しない場合、空の列を作成

    df_processed = df.drop(index=[0, 1])
    df_processed = df_processed[columns_required]
    menu_columns = [
        "主食（パン・ごはん）",
        "献立名１",
        "献立名２",
        "献立名３",
        "献立名４",
        "献立名５",
        "献立名６",
        "飲み物",
    ]
    df_processed[menu_columns] = df_processed[menu_columns].replace("★", "", regex=True)

    # 'menu_items' 配列を作成し、nullまたは空ではない文字列の献立名の値を追加
    df_processed["menu_items"] = df_processed[menu_columns].apply(
        lambda row: [
            str(item).strip() for item in row if not pd.isna(item) and str(item).strip()
        ],
        axis=1,
    )

    # 不要な列を削除
    df_processed.drop(menu_columns, axis=1, inplace=True)

    column_mapping = {
        "ic:年": "year",
        "ic:月": "month",
        "ic:日": "day",
        "主食（パン・ごはん）": "main_dish",
        "飲み物": "drink",
        "カロリー（小学校）": "calories_elementary",
        "カロリー（中学校）": "calories_junior_high",
    }

    df_processed.rename(columns=column_mapping, inplace=True)
    df_processed["offered_at"] = pd.to_datetime(
        df_processed[["year", "month", "day"]], errors="coerce"
    ).dt.strftime("%Y-%m-%d")
    df_processed.drop(["year", "month", "day"], axis=1, inplace=True)
    df_processed = df_processed[
        ~df_processed["calories_elementary"].isna()
        | ~df_processed["calories_junior_high"].isna()
    ]
    df_processed = df_processed[df_processed["menu_items"].str.len() > 0]

    return df_processed


# JSON形式で保存する関数
def save_to_json(df, output_file_path):
    json_data = df.to_json(orient="records", force_ascii=False)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(json_data)


# フォルダ内のすべてのファイルを処理する関数
def process_all_excel_files(input_directory, output_directory):
    # 入力ディレクトリ内のすべてのファイルを列挙
    for filename in os.listdir(input_directory):
        # .xlsファイルのみを対象とする
        if filename.endswith(".xls"):
            file_path = os.path.join(input_directory, filename)
            try:
                # エクセルファイルを処理
                df_processed = process_excel_file(file_path)
                # JSONデータをファイルに保存
                json_file_path = os.path.join(
                    output_directory, f"{os.path.splitext(filename)[0]}.json"
                )
                save_to_json(df_processed, json_file_path)
            except Exception as e:
                # エラーログを出力
                error_msg = (
                    f"Error processing file {filename}: {e}\n{traceback.format_exc()}"
                )
                print(error_msg)
                # エラーログをファイルに保存
                with open(
                    os.path.join(output_directory, "error_log.txt"),
                    "a",
                    encoding="utf-8",
                ) as log_file:
                    log_file.write(error_msg + "\n")


# 入力ディレクトリと出力ディレクトリのパスを指定
input_directory = "./data/input/menus/"
output_directory = "./data/output/menus/"

# 処理の実行
process_all_excel_files(input_directory, output_directory)
