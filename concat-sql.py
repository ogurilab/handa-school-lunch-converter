import os

# ディレクトリと結合後のファイルのパスを設定
directory_path = "./data/sql/complete/"
output_file_path = "./data/sql/results/2024-02-07.sql"

# 結合ファイルを開く
with open(output_file_path, "w") as combined_file:
    # ディレクトリ内の全ファイルをループ
    for filename in os.listdir(directory_path):
        # .sqlファイルのみを対象
        if filename.endswith(".sql"):
            # SQLファイルを開く
            with open(os.path.join(directory_path, filename), "r") as f:
                # SQLファイルの内容を読み込み、結合ファイルに書き込む
                combined_file.write(f.read() + "\n\n")  # ファイル間に空行を挿入
