# 半田市給食データ変換ツール

このツールは半田市の給食データが含まれた `.xls` ファイルを JSON 形式に変換するためのものです。データの前処理として、不要な行の削除、必要な列の選択、献立名から特定の記号の除去、列名の英語への翻訳が含まれます。
給食のデータは[LinkData](http://user.linkdata.org/user/kouhou_handacity/work)から取得してください。

## 前提条件

このスクリプトは Python 3 の環境で実行することを想定しています。依存関係のあるパッケージをインストールする前に、Python 3 がシステムにインストールされていることを確認してください。

## インストール

依存関係のあるパッケージは `requirements.txt` ファイルにリストされています。以下のコマンドを実行して、必要なパッケージをインストールしてください。

```bash
pip install -r requirements.txt
```

## 使用方法

input ファルダに変換したいファイルを入れて、以下のコマンドを実行してください。

```bash
python convert.py
```

## 出力

```JSON
[
  {
    "year": "2023",
    "month": "11",
    "day": "1",
    "main_dish": "ごはん",
    "menu_item_1": "みそ汁",
    "menu_item_2": "鮭の塩焼き",
    "menu_item_3": "ほうれん草のおひたし",
    "menu_item_4": null,
    "menu_item_5": null,
    "menu_item_6": null,
    "drink": "牛乳",
    "calories_elementary": "650",
    "calories_junior_high": "700"
  },
  ...
]

```
