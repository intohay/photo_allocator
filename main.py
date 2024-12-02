import json
import argparse

from create_input_from_csv import summarize_csv_file
from trade_photos import trade_photos
from visualizers.build_output_pdf import create_pdf


def main(csv_dir_path: str, m: int, debug_mode: bool):
    # csv_dir_path: マークシートのアプリで出力される CSVファイルが格納されるディレクトリパス
    # m: 参加者の人数
    # debug_mode: 出力される PDFにデバッグ情報を載せたもの。

    inputs = summarize_csv_file(csv_dir_path)

    input_file_path = "tmp/input.json"

    with open(input_file_path, "w", encoding="utf-8") as f:
        json.dump(inputs, f, ensure_ascii=False, indent=4)

    output_file_path = "tmp/output.json"
    trade_photos(
        m=m, input_file_path=input_file_path, output_file_path=output_file_path
    )

    with open(output_file_path, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    if debug_mode:
        # TODO
        pass
    else:
        create_pdf(filename="output/photo_info.pdf", output_data=output_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int, help="参加人数")
    parser.add_argument(
        "--test-mode",
        type=bool,
        default=False,
        help="データの参照先をテスト用のものにするオプション",
    )
    parser.add_argument(
        "--debug-mode",
        type=bool,
        default=False,
        help="PDF の出力に交換前のものも記載するオプション",
    )
    args = parser.parse_args()

    if args.test_mode:
        csv_dir_path = "data_for_test/"
    else:
        csv_dir_path = "data/"

    main(
        csv_dir_path=csv_dir_path,
        m=args.m,
        debug_mode=args.debug_mode,
    )
