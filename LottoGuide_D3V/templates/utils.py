import os
import sys

def resource_path(relative_path):
    """คืน path ที่ถูกต้องไม่ว่ารันจาก .py หรือ .exe"""
    try:
        # PyInstaller สร้างโฟลเดอร์ชั่วคราวและเก็บ path ใน _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # ถ้าไม่ได้รันจาก .exe ให้ใช้ path ปกติ
        # os.path.dirname(__file__) คือโฟลเดอร์ 'templates'
        # .dirname().dirname() คือรากของโปรเจกต์ (LottoGuide_D3V)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    return os.path.normpath(os.path.join(base_path, relative_path))