import csv
import glob
import os


def summarize_csv_file(dir_path: str):
    filenames = _get_csv_filenames(dir_path)

    # base_name(参加者名) の取得。ファイル名のバリデーションも行う。
    base_names = _retrieve_base_names_from_input_files(filenames)
    print("base_names:", base_names)

    inputs: list = []
    for base_name in base_names:
        quantities = _merge_csv_data(dir_path=dir_path, base_name=base_name)
        photos = _convert_with_photo_id(quantities)

        inputs.append({"name": base_name, "photos": photos})

    return inputs


def _get_csv_filenames(dir_path: str) -> list[str]:
    csv_files = glob.glob(os.path.join(dir_path, "*.csv"))

    return [os.path.basename(file) for file in csv_files]


def _retrieve_base_names_from_input_files(filenames: list[str]) -> list[str]:
    # 入力するファイルの命名は以下の通りとする
    # {base_name}1.csv, {base_name}2.csv
    # ただし、base_name は入力された名前
    # これらを合わしてすべての生写真についてのデータを持つ
    base_names = []

    # base_name の取得、および決められたフォーマットと違うものがあるかの確認
    for filename in filenames:
        if filename.endswith("1.csv"):
            base_name = filename[:-5]
            base_names.append(base_name)
        elif filename.endswith("2.csv"):
            continue
        else:
            raise Exception("input csv names are invalid: endswith 1.csv or 2.csv")

    # 各base_name に対し、決められたフォーマットのものが正しく存在することを確認
    for base_name in base_names:
        if f"{base_name}1.csv" not in filenames:
            raise Exception(
                f"input csv names are invalid: {base_name}1.csv is not exist"
            )
        if f"{base_name}2.csv" not in filenames:
            raise Exception(
                f"input csv names are invalid: {base_name}2.csv is not exist"
            )

    return base_names


def _merge_csv_data(dir_path, base_name: str) -> list[int]:
    quantities = []
    base_name_path = os.path.join(dir_path, base_name)
    with open(base_name_path + "1.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # CSVファイルの 1行目は不要な HEADER 情報なので捨てる
        next(reader)
        second_line = next(reader, None)
        # 2行目は以下のようなフォーマットで、"" のものは 0に、それ以外は int にキャストする
        # ただし、最初の 3つの値は使用しないので捨てる
        # "","","","3",...
        casted_second_line = [int(item) if item else 0 for item in second_line][3:]

        quantities += casted_second_line

        assert len(quantities) == 45, "data missing"

    with open(base_name_path + "2.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # CSVファイルの 1行目は不要な HEADER 情報なので捨てる
        next(reader)
        second_line = next(reader, None)
        # 2行目は以下のようなフォーマットで、"" のものは 0に、それ以外は int にキャストする
        # ただし、最初の 3つの値は使用しないので捨てる
        # "","","","3",...
        casted_second_line = [int(item) if item else 0 for item in second_line][3:]
        quantities += casted_second_line

        assert len(quantities) == 90, "data missing"

    return quantities


def _convert_with_photo_id(quantities: list[int]) -> dict:
    return {
        # NO WAR in the future
        "01-1": quantities[1],
        "01-2": quantities[2],
        "01-3": quantities[3],
        "01-4": quantities[4],
        # ハッピーオーラ
        "02-1": quantities[6],
        "02-2": quantities[7],
        "02-3": quantities[8],
        "02-4": quantities[9],
        # 君に話しておきたいこと
        "03-1": quantities[11],
        "03-2": quantities[12],
        "03-3": quantities[13],
        "03-4": quantities[14],
        # ひらがなくりすます
        "04-1": quantities[16],
        "04-2": quantities[17],
        "04-3": quantities[18],
        "04-4": quantities[19],
        # 青春の馬
        "05-1": quantities[21],
        "05-2": quantities[22],
        "05-3": quantities[23],
        "05-4": quantities[24],
        # おばけホテルメイド
        "06-1": quantities[26],
        "06-2": quantities[27],
        "06-3": quantities[28],
        "06-4": quantities[29],
        # 紅白
        "07-1": quantities[31],
        "07-2": quantities[32],
        "07-3": quantities[33],
        "07-4": quantities[34],
        # 恋魚
        "08-1": quantities[36],
        "08-2": quantities[37],
        "08-3": quantities[38],
        "08-4": quantities[39],
        # わんちょいす
        "09-1": quantities[41],
        "09-2": quantities[42],
        "09-3": quantities[43],
        "09-4": quantities[44],
        # ネイビーサンタ
        "10-1": quantities[46],
        "10-2": quantities[47],
        "10-3": quantities[48],
        "10-4": quantities[49],
        # さびけん
        "11-1": quantities[51],
        "11-2": quantities[52],
        "11-3": quantities[53],
        "11-4": quantities[54],
        # シークレット1
        "12-1": quantities[56],
        "12-2": quantities[57],
        "12-3": quantities[58],
        "12-4": quantities[59],
        # シークレット2
        "13-1": quantities[61],
        "13-2": quantities[62],
        "13-3": quantities[63],
        "13-4": quantities[64],
    }
