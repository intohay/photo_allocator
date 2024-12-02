def convert_outputs_to_display(output_data):
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


# photos = {
#     "01-1": "ORIGINALLY",
#     "01-2": "ORIGINALLY",
#     "01-3": "NOT",
#     "01-4": "ORIGINALLY",
#     "02-1": "NOT",
#     "02-2": "ORIGINALLY",
#     "02-3": "NOT",
#     "02-4": "ORIGINALLY",
#     "03-1": "NOT",
#     "03-2": "ORIGINALLY",
#     "03-3": "NOT",
#     "03-4": "ORIGINALLY",
#     "04-1": "NOT",
#     "04-2": "NOT",
#     "04-3": "NOT",
#     "04-4": "NOT",
#     "05-1": "NOT",
#     "05-2": "NOT",
#     "05-3": "NOT",
#     "05-4": "NOT",
#     "06-1": "NOT",
#     "06-2": "NOT",
#     "06-3": "ORIGINALLY",
#     "06-4": "ORIGINALLY",
#     "07-1": "NOT",
#     "07-2": "NOT",
#     "07-3": "NOT",
#     "07-4": "NOT",
#     "08-1": "NOT",
#     "08-2": "NOT",
#     "08-3": "NOT",
#     "08-4": "NOT",
#     "09-1": "NOT",
#     "09-2": "NOT",
#     "09-3": "NOT",
#     "09-4": "NOT",
#     "10-1": "ORIGINALLY",
#     "10-2": "ORIGINALLY",
#     "10-3": "NOT",
#     "10-4": "ORIGINALLY",
#     "11-1": "NOT",
#     "11-2": "ORIGINALLY",
#     "11-3": "NOT",
#     "11-4": "ORIGINALLY",
#     "12-1": "NOT",
#     "12-2": "ORIGINALLY",
#     "12-3": "NOT",
#     "12-4": "ORIGINALLY",
#     "13-1": "NOT",
#     "13-2": "NOT",
#     "13-3": "NOT",
#     "13-4": "NOT",
# }

# print(convert_outputs_to_display(photos))
