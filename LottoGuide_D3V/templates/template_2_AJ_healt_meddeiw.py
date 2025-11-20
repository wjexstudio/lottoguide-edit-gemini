from .utils import resource_path

TEMPLATE_NAME = "เม็ดเดียวปลดหนี้"
TEMPLATE_IMAGE = resource_path("assets/pic/ใบแนวทางอาจารย์แห้ว-เม็ดเดียว.png")
TEMPLATE_ORDER = 2

POSITIONS = [
    (880, 400, 'TITLE'),
    (900, 2150, 'CLOSING_TIME'),
    (880, 200, 'DATE'),
    (880, 635, 5),
    (880, 1040, 1),  # ตัวเดียวกลาง
]

FONT_SIZES = {
    "TITLE": 95,
    "CLOSING": 50,
    "DATE": 80,
    "FIVE": 140,
    "ONE": 260,
}

OUTPUT_WIDTH = None
OUTPUT_HEIGHT = None

LOTTO_LIST = [
    "ลาวพัฒนา ปิดรับ 20.20 น."
]