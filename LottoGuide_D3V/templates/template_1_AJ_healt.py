from .utils import resource_path

TEMPLATE_NAME = "ชุดเต็ม"
TEMPLATE_IMAGE = resource_path("assets/pic/ใบแนวทางอาจารย์แห้ว.png")
TEMPLATE_ORDER = 1

POSITIONS = [
    (880, 400, 'TITLE'),
    (900, 2150, 'CLOSING_TIME'),
    (880, 200, 'DATE'),
    (880, 635, 5),
    (380, 1040, 1), (1370, 1040, 1),
    (390, 1380, 2), (900, 1380, 2), (1370, 1380, 2),
    (390, 1660, 2), (900, 1660, 2), (1370, 1660, 2),
    (390, 1970, 3), (880, 1970, 3), (1370, 1970, 3)
]

FONT_SIZES = {
    "TITLE": 95,
    "CLOSING": 50,
    "DATE": 80,
    "FIVE": 140,
    "ONE": 240,
    "TWO": 140,
    "THREE": 140,
}

OUTPUT_WIDTH = None
OUTPUT_HEIGHT = None

LOTTO_LIST = [
    "ลาวพัฒนา ปิดรับ 20.20 น."
]