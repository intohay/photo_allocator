import json
import random
import numpy as np
import sys


def generate_random_data(num_users, output_file):
    n = 52
    q = [random.randint(11, 15) * 5 for _ in range(num_users)]

    packs = [qi // 5 for qi in q]
    A = [np.zeros(n, dtype=int) for _ in range(num_users)]

    for i in range(num_users):
        # カードパックを引く
        cards = []
        for _ in range(packs[i]):
            pack = np.random.choice(range(n), size=5, replace=False)
            cards.extend(pack)

        # 所持カードを更新
        for card in cards:
            A[i][card] += 1

    print(A)

    data = []
    for i in range(1, num_users + 1):
        user_data = {"name": f"ユーザ{i}", "photos": {}}
        for costume in range(1, 14):  # 01 to 13
            for pose in range(1, 5):  # 1 to 4
                key = f"{costume:02d}-{pose}"
                user_data["photos"][key] = int(A[i - 1][(costume - 1) * 4 + pose - 1])
        data.append(user_data)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    args = sys.argv

    if len(args) < 2:
        print("Usage: python generate_dummy.py num_users")
        sys.exit(1)

    num_users = int(args[1])
    output_file = "input.json"

    generate_random_data(num_users, output_file)

    print(f"Generated random data for {num_users} users and saved to {output_file}")
