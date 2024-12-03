from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)

from .converter import convert_outputs_to_display


pdfmetrics.registerFont(
    TTFont("NotoSerifJP-ExtraBold", "fonts/Noto_Serif_JP/NotoSerifJP-ExtraBold.ttf")
)
pdfmetrics.registerFont(
    TTFont("NotoSerifJP-Regular", "fonts/Noto_Serif_JP/NotoSerifJP-Regular.ttf")
)
styles = getSampleStyleSheet()

custom_styles = {
    "title": ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName="NotoSerifJP-ExtraBold",
        fontSize=18,
        textColor=colors.black,
        spaceAfter=12,
    ),
    "description": ParagraphStyle(
        "CustomDescription",
        parent=styles["Normal"],
        fontName="NotoSerifJP-Regular",
        fontSize=12,
        textColor=colors.black,
        spaceAfter=12,
    ),
    "table": TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # ヘッダー行の背景色
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # ヘッダー行の文字色
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "NotoSerifJP-ExtraBold",
            ),  # ヘッダー行のフォント
            ("BOTTOMPADDING", (0, 0), (-1, 0), 4),  # ヘッダー行の下の余白
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "NotoSerifJP-Regular",
            ),  # データ行のフォント
        ]
    ),
    "difference": ParagraphStyle(
        "Difference", fontName="NotoSerifJP-Regular", fontSize=10, leading=12
    ),
}


description_text = """
生写真トレードで獲得できるものをまとめた表です。<br/>
<br/>
✓：すでに手元にあるはずの生写真<br/>
□：山札から 1枚取ることができる生写真<br/>
空欄：トレードに参加していない方とトレードしてください

"""


def create_pdf(filename, output_data, num_photos_map):
    # PDFのドキュメントを作成
    pdf = SimpleDocTemplate(filename, pagesize=A4)

    elements = []

    for personal_data in output_data:
        # タイトル用のスタイルを定義
        title = Paragraph(f"{personal_data['name']} さん", custom_styles["title"])

        description = Paragraph(
            description_text,
            custom_styles["description"],
        )

        # テーブルを作成
        converted_output_data = convert_outputs_to_display(personal_data)
        table = Table(converted_output_data)

        # テーブルスタイルを設定
        style = custom_styles["table"]

        # 偶数行にハイライトを入れる
        for row_num in range(1, len(converted_output_data)):
            bg_color = colors.whitesmoke if row_num % 2 == 0 else colors.white
            style.add("BACKGROUND", (0, row_num), (-1, row_num), bg_color)
        table.setStyle(style)

        before = num_photos_map[personal_data["name"]]
        after = personal_data["total"]
        difference_paragraph = Paragraph(
            f"エントリー枚数: {before}枚, 重複無しで配布する枚数: {after}枚, 山札から引ける枚数: {before - after}枚",
            custom_styles["difference"],
        )

        # PDFにテーブルと差の情報を追加
        elements.extend(
            [
                title,
                Spacer(1, 12),
                description,
                Spacer(1, 24),
                table,
                Spacer(1, 12),
                difference_paragraph,
                PageBreak(),
            ]
        )

    pdf.build(elements)
