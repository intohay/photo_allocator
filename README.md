# Photo Allocator

生写真を公平に分配するシステム

## Installation

1. リポジトリをクローンする
```
git clone https://github.com/yourusername/PhotoAllocator.git
cd PhotoAllocator
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

## Allocation

以下のコードで最終的な結果が`output.json`として出力される。
```
python photo_trading.py <your input json file>
```








