import pulp
import numpy as np
import pandas as pd
import json
import sys


# AテーブルとBテーブルをデータフレームで表示する関数
def display_state(A, B, n, m, label="状態"):
    # Aテーブル（カード保持状況）
    A_array = np.array(A)
    A_df = pd.DataFrame(
        A_array,
        index=[f"Person_{i}" for i in range(m)],
        columns=[f"Card_{j}" for j in range(n)],
    )
    print(f"\n{label}のAテーブル（カード保持状況）：")
    print(A_df.T)  # 転置してカードを行、人物を列にする

    # personごとのカード数
    person_card_counts = A_array.sum(axis=1)
    print("\n各人のカード数：")
    for i, count in enumerate(person_card_counts):
        print(f"Person_{i}:　{count} 枚")

    # 最大値と最小値、そしてその差
    print("\nカード数の最大値：", person_card_counts.max())
    print("カード数の最小値：", person_card_counts.min())
    print(
        "カード数の最大値と最小値の差：",
        person_card_counts.max() - person_card_counts.min(),
    )

    # Bテーブル（場のカード状況）
    B_df = pd.DataFrame(
        B, index=[f"Card_{j}" for j in range(n)], columns=["場のカード"]
    )
    print(f"\n{label}のBテーブル（場のカード状況）：")
    print(B_df)


def minimize_max_min_difference(p, fixed_ones, n, m):
    # 問題の作成
    prob = pulp.LpProblem("Minimize_Max_Min_Difference", pulp.LpMinimize)

    # 変数の定義
    a = {}
    for i in range(n):
        for j in range(m):
            var_name = f"a_{i}_{j}"
            a[i, j] = pulp.LpVariable(var_name, 0, 1, pulp.LpBinary)

    # 固定された変数に対する制約の追加
    for i, j in fixed_ones:
        prob += a[i, j] == 1, f"Fixed_{i}_{j}"

    # 列の合計を表す変数
    S = {}
    for j in range(m):
        S[j] = pulp.LpVariable(f"S_{j}", 0, n, pulp.LpInteger)

    # 最大値と最小値を表す変数
    max_S = pulp.LpVariable("max_S", 0, n, pulp.LpInteger)
    min_S = pulp.LpVariable("min_S", 0, n, pulp.LpInteger)

    # 目的関数
    prob += max_S - min_S, "Minimize_Max_Min_Difference"

    # 制約条件
    # 行の合計制約（各カードは最大で m 人にしか配れない）
    for i in range(n):
        prob += pulp.lpSum([a[i, j] for j in range(m)]) == min(p[i], m), f"Row_Sum_{i}"

    # 列の合計と a_ij の関連付け
    for j in range(m):
        prob += S[j] == pulp.lpSum([a[i, j] for i in range(n)]), f"Col_Sum_{j}"

    # 最大値と最小値の制約
    for j in range(m):
        prob += S[j] <= max_S, f"Max_S_Constraint_{j}"
        prob += S[j] >= min_S, f"Min_S_Constraint_{j}"

    # 問題の解決
    solver = pulp.PULP_CBC_CMD(msg=False)
    result = prob.solve(solver)

    # 最適解のチェック
    if result != pulp.LpStatusOptimal:
        print("最適解が見つかりませんでした。")
        return None

    # 最適値の取得
    solution = {
        "a_ij": {(i, j): pulp.value(a[i, j]) for i in range(n) for j in range(m)},
        "S_j": {j: pulp.value(S[j]) for j in range(m)},
        "max_S": pulp.value(max_S),
        "min_S": pulp.value(min_S),
        "Objective": pulp.value(prob.objective),
    }

    return solution


def export_to_json(A, status, names, output_file="output.json"):
    """
    最終状態を指定されたJSON形式で出力する関数。
    """
    output_data = []

    for i, name in enumerate(names):
        person_data = {
            "name": name,
            "total": int(np.sum(A[i])),  # 各人が持っているカードの合計数
            "photos": {},
        }

        for j in range(len(A[i])):
            card_id = f"{(j // 4) + 1:02d}-{(j % 4) + 1}"
            person_data["photos"][card_id] = status[i][j]  # カードの状態を追加

        output_data.append(person_data)

    # JSONファイルとして保存
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"JSONファイルに出力しました: {output_file}")


# 使用例
if __name__ == "__main__":

    # random.seed(42)

    # コマンドライン引数としてjsonのパスを受け取る
    if len(sys.argv) != 2:
        print("Usage: python photo_trading.py input.json")
        sys.exit(1)

    input_file_path = sys.argv[1]
    with open(input_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 初期化
    m = len(data)  # 人数
    n = 52  # カード種類
    # 55以上のランダムな5の倍数をm個生成
    # q = [random.randint(11, 15) * 5 for _ in range(m)]

    # packs = [qi // 5 for qi in q]  # 各人のカードパック数
    A = [np.zeros(n, dtype=int) for _ in range(m)]
    status = [["NOT" for _ in range(n)] for _ in range(m)]

    # 場の重複カードテーブル (B)
    B = np.zeros(n, dtype=int)

    for person in data:
        for key, value in person["photos"].items():
            card_id = (int(key[:2]) - 1) * 4 + int(key[-1]) - 1
            A[data.index(person)][card_id] = 1 if value > 0 else 0
            B[card_id] += value - 1 if value > 1 else 0

            status[data.index(person)][card_id] = "ORIGINALLY" if value > 0 else "NOT"

    initial_sum = sum(A[i].sum() for i in range(m)) + B.sum()
    initial_sum_per_type = [sum(A[i][j] for i in range(m)) + B[j] for j in range(n)]

    # シミュレーション
    # np.random.seed(42)  # 再現性のため
    # for i in range(m):
    #     # カードパックを引く
    #     cards = []
    #     for _ in range(packs[i]):
    #         pack = np.random.choice(range(n), size=5, replace=False)
    #         cards.extend(pack)

    #     # 所持カードを更新
    #     for card in cards:
    #         if A[i][card] == 1:  # すでに持っている場合は場に送る
    #             B[card] += 1
    #         else:
    #             A[i][card] = 1

    # 初期状態の表示
    display_state(A, B, n, m, label="初期")

    # 場のカードを分配
    for j in range(n):
        # A_i[j] = 0 の人数を数える
        zero_count = sum(1 for i in range(m) if A[i][j] == 0)

        # 分配条件を満たす場合のみ分配
        if B[j] >= zero_count:
            for i in range(m):
                if A[i][j] == 0 and B[j] > 0:
                    A[i][j] = 1
                    B[j] -= 1
                    status[i][j] = "GIVEN"
        # else:
        #     S = [(i, sum(1 for j in range(n) if A[i][j] == 0)) for i in range(m)]
        #     S.sort(key=lambda x: x[1])

        #     for i, _ in S:
        #         if A[i][j] == 0 and B[j] > 0:
        #             A[i][j] = 1
        #             B[j] -= 1

    display_state(A, B, n, m, label="1次分配後")

    fixed_ones = {(i, j) for j in range(m) for i in range(n) if A[j][i] == 1}

    p = []
    for i in range(n):
        total = min(B[i] + sum(A[j][i] for j in range(m)), m)
        p.append(total)
    p = np.array(p)

    # 最適化
    solution = minimize_max_min_difference(p, fixed_ones, n, m)

    if solution is not None:

        # 最適解の適用
        for i in range(n):
            for j in range(m):
                if A[j][i] == 0 and solution["a_ij"][i, j] == 1:
                    status[j][i] = "GIVEN"
                    B[i] -= 1

                A[j][i] = solution["a_ij"][i, j]

                if (i, j) in fixed_ones:
                    assert A[j][i] == 1

        display_state(A, B, n, m, label="最終")

    else:
        print("最適解が見つかりませんでした。")

    names = [person["name"] for person in data]
    export_to_json(A, status, names, output_file="output.json")

    # 検証

    final_sum = sum(A[i].sum() for i in range(m)) + B.sum()

    print(f"\n最初の全体の枚数：{initial_sum}")
    print(f"最終の全体の枚数：{final_sum}")

    # 最初の全体の枚数と最後の全体の枚数は等しい
    assert initial_sum == sum(A[i].sum() for i in range(m)) + B.sum()

    final_sum_per_type = [sum(A[i][j] for i in range(m)) + B[j] for j in range(n)]

    print("\n各カードの枚数：")
    for j in range(n):
        print(f"Card_{j}: {initial_sum_per_type[j]} → {final_sum_per_type[j]}")

    # それぞれの種類のカードの総数はそれぞれ最初と最後で等しい
    for j in range(n):
        assert initial_sum_per_type[j] == sum(A[i][j] for i in range(m)) + B[j]
