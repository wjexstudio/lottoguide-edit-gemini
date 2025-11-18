# 💡 [แก้ไข] ลบ os, sys, importlib และการค้นหาไฟล์อัตโนมัติออก

# 💡 [แก้ไข] 1. Import เทมเพลตทั้งหมดของคุณด้วยมือ (Manual Import)
from . import template_1_AJ_healt
from . import template_2_AJ_healt_meddeiw
from . import template_3_puyaijaidee
from . import template_4_baansedteeparuay

# 💡 [แก้ไข] 2. สร้างลิสต์ของโมดูลที่ Import เข้ามา
_template_modules = [
    template_1_AJ_healt,
    template_2_AJ_healt_meddeiw,
    template_3_puyaijaidee,
    template_4_baansedteeparuay
]

TEMPLATES = []

# 💡 [แก้ไข] 3. ลูปจากลิสต์ที่สร้างขึ้นแทน os.listdir
for module in _template_modules:
    try:
        template_config = {
            "name": module.TEMPLATE_NAME,
            "image": module.TEMPLATE_IMAGE,
            "positions": module.POSITIONS,
            "font_sizes": module.FONT_SIZES,
            "output_height": module.OUTPUT_HEIGHT,
            "output_width": module.OUTPUT_WIDTH,
            "order": getattr(module, "TEMPLATE_ORDER", 99)
        }
        TEMPLATES.append(template_config)
        
    except AttributeError as e:
        print(f"❌ WARNING: เกิดข้อผิดพลาดในการโหลด {module.__name__}: {e}")
            
# 💡 เรียงลำดับ TEMPLATES (เหมือนเดิม)
TEMPLATES.sort(key=lambda t: t['order'])

# 💡 [แก้ไข] ลบ resource_path ออกจากไฟล์นี้
__all__ = ["TEMPLATES"]