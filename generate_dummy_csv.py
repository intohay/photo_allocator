import csv
import os
import random
from dotenv import load_dotenv

load_dotenv()


def main():
    m = int(os.getenv("NUM_USERS"))

    if not os.path.exists("data_for_test"):
        os.makedirs("data_for_test")

    # データを生成する前にすべて消去しておく
    # 理由: 前回生成した CSVが残ると、想定の参加者数より多くなってしまうため
    for filename in os.listdir("data_for_test"):
        file_path = os.path.join("data_for_test", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # 1パック 5枚入り
    num_photos = 5 * int(os.getenv("NUM_PACKS"))

    for i in range(m):
        photo_counter = [0] * 52
        for _ in range(num_photos):
            # 大きな乱数を生成し、それを53で割った余りをインデックスとして使用
            random_index = random.randint(0, 10**6) % 52
            photo_counter[random_index] += 1

        assert sum(photo_counter) == num_photos, "allocation missing"

        random_data = [str(i) if i != 0 else "" for i in photo_counter]

        csv_data = _generate_csv_data(random_data)

        header = [row[0] for row in csv_data]  # ヘッダー行
        first = [row[1] for row in csv_data]  # 1-9 個目の衣装
        second = [row[2] for row in csv_data]  # 10-13 個目の衣装

        base_name = "濱岸ヲタ" + chr(65 + i)
        print("create user:", base_name)
        with open(
            f"data_for_test/{base_name}1.csv", "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(first)

        with open(
            f"data_for_test/{base_name}2.csv", "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(second)


def _generate_csv_data(random_data: list[str]) -> list:
    assert len(random_data) == 52, "random_data length is invalid"
    return [
        # 見やすさのため、列と行を入れ替えたものを定義する
        # 1列目が CSVファイルのヘッダー
        # 2列目が 1-9個目の衣装の枚数
        # 3列目が 10-13個目の衣装の枚数
        # 使わないデータ
        ["�N", "", ""],
        ["�g", "", ""],
        ["�ԍ�", "", ""],
        # NO WAR in the future
        ["��1", "", ""],
        ["��2", random_data[0], random_data[36]],
        ["��3", random_data[1], random_data[37]],
        ["��4", random_data[2], random_data[38]],
        ["��5", random_data[3], random_data[39]],
        #
        ["��6", "", ""],
        ["��7", random_data[4], random_data[40]],
        ["��8", random_data[5], random_data[41]],
        ["��9", random_data[6], random_data[42]],
        ["��10", random_data[7], random_data[43]],
        #
        ["��11", "", ""],
        ["��12", random_data[8], random_data[44]],
        ["��13", random_data[9], random_data[45]],
        ["��14", random_data[10], random_data[46]],
        ["��15", random_data[11], random_data[47]],
        #
        ["��16", "", ""],
        ["��17", random_data[12], random_data[48]],
        ["��18", random_data[13], random_data[49]],
        ["��19", random_data[14], random_data[50]],
        ["��20", random_data[15], random_data[51]],
        #
        ["��21", "", ""],
        ["��22", random_data[16], ""],
        ["��23", random_data[17], ""],
        ["��24", random_data[18], ""],
        ["��25", random_data[19], ""],
        #
        ["��26", "", ""],
        ["��27", random_data[20], ""],
        ["��28", random_data[21], ""],
        ["��29", random_data[22], ""],
        ["��30", random_data[23], ""],
        #
        ["��31", "", ""],
        ["��32", random_data[24], ""],
        ["��33", random_data[25], ""],
        ["��34", random_data[26], ""],
        ["��35", random_data[27], ""],
        #
        ["��36", "", ""],
        ["��37", random_data[28], ""],
        ["��38", random_data[29], ""],
        ["��39", random_data[30], ""],
        ["��40", random_data[31], ""],
        #
        ["��41", "", ""],
        ["��42", random_data[32], ""],
        ["��43", random_data[33], ""],
        ["��44", random_data[34], ""],
        ["��45", random_data[35], ""],
    ]


if __name__ == "__main__":
    main()
