# Photo Allocator

生写真を公平に分配するシステム

## Installation

1. リポジトリをクローンする
```
git clone https://github.com/intohay/photo_allocator.git
cd photo_allocator
```

2. 必要なパッケージをインストールする(Pythonのバージョンは3.8以上を推奨)
```
pip install -r requirements.txt
```

3. 入力データのJSONファイルを用意する。

構造は以下の通り。
```
[
    {
        "name": "ユーザ1",
        "photos": {
            "01-1": 1,
            "01-2": 3,
            "01-3": 0,
            "01-4": 0,
            "02-1": 1,
            "02-2": 4,
            "02-3": 0,
            "02-4": 0,
            …
        }
    },
    {
        "name": "ユーザ2",
        "photos": {
            "01-1": 2,
            "01-2": 2,
            "01-3": 0,
            "01-4": 2,
            "02-1": 1,
            "02-2": 0,
            "02-3": 0,
            "02-4": 1,
            …
        }
    },…
]
```

`generate_dummy.py`を使ってダミーの入力データを生成できる。以下はトレードする人数が12人である入力データを生成する例：

```
python generate_dummy.py 12
```

`generate_dummy_csv.py` を使ってダミーのCSVファイルを生成できる。
```
python generate_dummy_csv.py
```

## Allocation

以下のコードで最終的な結果が`output.json`として出力される。
```
python photo_trading.py <your input json file>
```

以下のコードで通しの処理が走る。
```
python main.py --test-mode True --debug-mode True
```

引数について
- --test-mode は、マークシートのアプリが出力したCSVファイルの参照先を変更するためのオプション
    - True の場合は data_for_test/ のファイルを参照する
    - False の場合は data/ のファイルを参照する。(本番ではこちらを使う)
    - default は False
- --debug-mode は、出力する PDFの内容を変更するためのオプション
    - True の場合は output の情報に加え、input の情報や、その他のサマリーを出す(未実装)
    - False の場合は output の情報のみ出力する。(本番ではこちらを使う)
    - default は False


## Formatter
以下のコマンドで Python のコードを整形する。
```
black .
```




