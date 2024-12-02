song_titles = [
    "NO WAR in the future",
    "ハッピーオーラ",
    "君に話しておきたいこと",
    "ひらがなくりすます",
    "青春の馬",
    "おばけホテルメイド",
    "紅白",
    "恋魚",
    "わんちょいす",
    "ネイビーサンタ",
    "さびけん",
    "シークレット1",
    "シークレット2",
]


def convert_outputs_to_display(output_data):

    # 変換ルール
    def convert_status(status):
        if status == "ORIGINALLY":
            return "✓"
        elif status == "GIVEN":
            return "□"
        elif status == "NOT":
            return ""
        else:
            return ""

    # 変換結果を格納するリスト
    converted_data = [["曲名", "ヒキ", "チュウ", "ヨリ", "座り"]]

    print(output_data)
    # 各曲の写真状態を変換
    for i, title in enumerate(song_titles, start=1):
        row = [title]
        for j in range(1, 5):
            key = f"{i:02}-{j}"
            print("output", output_data)
            print("key", key)
            status = output_data["photos"][key]
            row.append(convert_status(status))
        converted_data.append(row)

    return converted_data


def convert_inputs_to_display(photos):
    # 変換結果を格納するリスト
    converted_data = [["曲名", "ヒキ", "チュウ", "ヨリ", "座り"]]

    # 各曲の写真状態を変換
    for i, title in enumerate(song_titles, start=1):
        row = [title]
        for j in range(1, 5):
            key = f"{i:02}-{j}"
            row.append(photos[key])
        converted_data.append(row)

    return converted_data
