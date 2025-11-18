# ============================================================
# 🎯 Lotto Guide Generator (ฉบับแก้ไขและปรับปรุง)
# ✅ โค้ดถูกปรับให้ 1 Template สร้างภาพสำหรับทุกชื่อหวยตามจำนวนชุดที่กำหนด
# ✅ แก้ไขการวนลูปซ้ำซ้อนและ Progress Bar
# ✅ แก้ไข NameError โดยย้าย resource_path ไปที่ __init__.py และ import กลับมา
# ============================================================

import os
import sys
import random
import threading
import json # Import json สำหรับอ่านไฟล์ Config
from datetime import datetime, timedelta
import ttkbootstrap as tb
from customtkinter import CTkButton, CTkSwitch
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk # 💡 [แก้ไข] ลบ ttk ออก
from PIL import Image, ImageDraw, ImageFont, ImageTk
from templates import TEMPLATES
# 💡 [แก้ไข] ลบบรรทัด 'from templates import resource_path' ที่ซ้ำซ้อนออก
from templates.utils import resource_path # Import 'resource_path' จาก 'templates.utils'

# -----------------------
# 🧩 ค่าตั้งต้นของระบบ
# -----------------------
THEME_COLOR = "#1E1E1E"      # สีพื้นหลังหลักของ GUI
HIGHLIGHT = "#FF8800"        # สีเน้น เช่น ปุ่มหรือหัวข้อ
THUMBNAIL_SIZE = (200, 230)    # ขนาดภาพตัวอย่าง Template
DEFAULT_IMAGE = TEMPLATES[0]["image"]


DEFAULT_OUTPUT = "output"              # โฟลเดอร์บันทึกผลลัพธ์
CONFIG_DIR = resource_path("configs")  # กำหนดโฟลเดอร์สำหรับเก็บไฟล์ .json
DEFAULT_DATE = ""                      # วันที่ (ถ้าไม่กรอก)
OUTPUT_WIDTH = 1410
OUTPUT_HEIGHT = 2000

# 💡 [ลบ] ขนาด Canvas ที่ไม่จำเป็นสำหรับ main.py
# CANVAS_MAX_WIDTH = 900
# CANVAS_MAX_HEIGHT = 700

# -----------------------
# 🔢 รายการหวยทั้งหมด
# -----------------------

# ย้าย def load_raw_list มาไว้ข้างบนก่อนเรียกใช้
def load_raw_list(file_path):
    """โหลดรายการหวยจากไฟล์"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"⚠️ ไม่พบไฟล์รายการหวยที่: {file_path}")
        return [
            "ลาวพัฒนาชุดเต็ม ปิดรับ 20.20น.",
            "ลาวพัฒนาเม็ดเดียว ปิดรับ 20.20น.",
            "หุ้นอียิปปปปปปป ปิดรับ 10.20น."
        ]

# เรียกใช้ load_raw_list *หลังจาก* ที่ def แล้ว
RAW_LIST = load_raw_list(resource_path("assets/lotto_list.txt"))
    
# สร้างรายการชื่อและเวลาปิดรับ (ข้ามรายการที่ไม่มีเวลา)
CUSTOM_TITLES = []
CLOSING_TIME = []
for item in RAW_LIST:
    if "ปิดรับ" in item:
        # แยกชื่อก่อนคำว่า "ปิดรับ"
        parts = item.split(" ปิดรับ")
        CUSTOM_TITLES.append(parts[0])
        CLOSING_TIME.append("ปิดรับ" + parts[1])
    else:
        # ถ้าไม่มีคำว่า "ปิดรับ" → เก็บชื่อไว้ แต่เวลาว่าง
        CUSTOM_TITLES.append(item)
        CLOSING_TIME.append("")

OUTPUT_COUNT = len(CUSTOM_TITLES)  # จำนวนชื่อหวยทั้งหมด

# -----------------------
# ตั้งค่าขนาดฟอนต์ต่าง ๆ FONT SETTINGS
# -----------------------
FONT_SIZE_CUSTOM_TITLE = 95
FONT_SIZE_CLOSING_TIME = 50
FONT_SIZE_DATE = 80
FONT_SIZE_5_DIGITS = 140
FONT_SIZE_1_DIGIT = 240
FONT_SIZE_2_DIGITS = 140
FONT_SIZE_3_DIGITS = 140

# แก้ไข Path ฟอนต์ให้ถูกต้อง (ตัดชื่อโฟลเดอร์แม่ออก)
DEFAULT_FONT = resource_path("assets/font/DB ThongLor X Bd.ttf")
H2_FONT = resource_path("assets/font/DB ThongLor X Bd.ttf")

# -----------------------
# 📍 จุดพิกัดวางข้อความบนภาพ
# -----------------------
ORIGINAL_POSITIONS = [
    (880, 400, 'TITLE'),
    (900, 2150, 'CLOSING_TIME'),
    (880, 200, 'DATE'),
    (880, 635, 5),
    (380, 1040, 1), (1370, 1040, 1),
    (390, 1380, 2), (900, 1380, 2), (1370, 1380, 2),
    (390, 1660, 2), (900, 1660, 2), (1370, 1660, 2),
    (390, 1970, 3), (880, 1970, 3), (1370, 1970, 3)
]

# ============================================================
# 💡ฟังก์ชันสำหรับโหลด/บันทึกไฟล์ JSON
# ============================================================

def get_safe_template_name(template_name):
    """สร้างชื่อไฟล์ที่ปลอดภัยจากชื่อเทมเพลต"""
    return template_name.replace(" ", "_").replace("/", "-").replace(":", "-").replace(".", "-")

def load_custom_positions(template_name):
    """
    โหลดตำแหน่งที่กำหนดเองจากไฟล์ .json
    ถ้าไม่เจอไฟล์ .json จะ return None
    """
    # สร้างโฟลเดอร์ configs ถ้ายังไม่มี
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        
    safe_name = get_safe_template_name(template_name)
    config_file = os.path.join(CONFIG_DIR, f"{safe_name}.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                positions = json.load(f)
                print(f"💡 โหลดตำแหน่งที่กำหนดเองสำหรับ '{template_name}' จาก {config_file}")
                
                # 💡 [แก้ไข] ตรวจสอบ Format ของ .json ที่อ่านได้
                # ต้องเป็น List (ชั้นนอก) และข้างในเป็น List ทั้งหมด (ชั้นใน)
                if isinstance(positions, list) and all(isinstance(item, list) for item in positions):
                    return positions
                else:
                    print(f"⚠️ Format ของ JSON '{config_file}' ไม่ถูกต้อง (ควรเป็น List of Lists) ใช้ค่าเริ่มต้นแทน")
                    return None
        except json.JSONDecodeError as e:
            # แจ้งเตือนถ้าไฟล์ .json ไวยากรณ์ผิด (เช่น มี 'POSITIONS =')
            print(f"⚠️ ไม่สามารถโหลดไฟล์ JSON '{config_file}' (ไฟล์อาจมี Format ผิด): {e}. ใช้ค่าเริ่มต้นแทน")
            return None
        except Exception as e:
            print(f"⚠️ ไม่สามารถโหลดไฟล์ JSON '{config_file}': {e}. ใช้ค่าเริ่มต้นแทน")
            return None
    return None # ไม่พบไฟล์ Config

def save_custom_positions(template_name, positions_list):
    """
    บันทึกตำแหน่ง (List) ลงในไฟล์ .json
    (ฟังก์ชันนี้จะถูกเรียกใช้โดย Editor ที่เราจะสร้างทีหลัง)
    """
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        
    safe_name = get_safe_template_name(template_name)
    config_file = os.path.join(CONFIG_DIR, f"{safe_name}.json")
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            # 💡 [แก้ไข] แปลง tuple (x, y, 'TYPE') เป็น list [x, y, 'TYPE'] ก่อนบันทึก
            # เพื่อให้เป็น Format JSON ที่ถูกต้อง
            list_to_save = [[item[0], item[1], item[2]] for item in positions_list]
            json.dump(list_to_save, f, indent=4)
            print(f"💾 บันทึกตำแหน่งที่กำหนดเองสำหรับ '{template_name}' ไปที่ {config_file}")
            return True
    except Exception as e:
        print(f"❌ ไม่สามารถบันทึกไฟล์ JSON '{config_file}': {e}")
        return False

# ============================================================
# 🧮 ฟังก์ชันสุ่มตัวเลขหวย
# ============================================================
def generate_lotto_numbers(used_five_digit_numbers):
    # ... (ฟังก์ชัน generate_lotto_numbers เหมือนเดิม)
    """
    ✅ ฟังก์ชันสุ่มชุดเลข 5 หลัก โดยไม่ให้ซ้ำกับที่เคยใช้
    พร้อมสร้างตัวเด่น ตัวรอง และชุดเลข 2 หลัก
    """
    attempt = 0
    five_digits = ""
    # 🔁 สุ่มเลขจนได้ชุดที่ไม่ซ้ำ
    while not five_digits or five_digits in used_five_digit_numbers:
        digits = random.sample(range(10), 5)
        five_digits = "".join(map(str, digits))
        attempt += 1
        if attempt > 200:
            break
    used_five_digit_numbers.add(five_digits)

    # ตัวเด่นคือตัวแรกของชุด
    left_single = five_digits[0]

    # ตัวรองคือสุ่มจากตัวอื่นในชุด
    remaining_digits = [d for d in five_digits if d != left_single]
    right_single = random.choice(remaining_digits) if remaining_digits else left_single

    # สร้างชุดเลข 2 หลัก (บน/ล่าง)
    unused_for_pairs = [d for d in five_digits if d not in [left_single, right_single]]
    top_pairs = [left_single + d for d in unused_for_pairs]
    bottom_pairs = [right_single + d for d in unused_for_pairs]

    # คืนค่าผลลัพธ์ทั้งหมดเป็น dict
    return {
        "five_digits": five_digits,
        "left_single": left_single,
        "right_single": right_single,
        "top_pairs": top_pairs,
        "bottom_pairs": bottom_pairs
    }

def generate_three_digit_sets(five_digits, left_single, right_single):
    # ... (ฟังก์ชัน generate_three_digit_sets เหมือนเดิม)
    """
    ✅ ฟังก์ชันสร้างเลข 3 หลัก 3 ชุด จากเลข 5 หลัก
    โดยไม่มีเลขซ้ำ และใช้ตัวเด่น/รองเป็นหลัก
    """
    # เอาตัวเลขที่เหลือจากตัวเด่น/รอง
    available_digits = [d for d in five_digits if d not in [left_single, right_single]]
    three_sets = []

    # สร้างชุด 3 หลัก 2 ชุดแรก (ขึ้นต้นด้วยตัวเด่น)
    for idx in range(len(available_digits) - 1):
        three_sets.append(left_single + available_digits[idx] + available_digits[idx + 1])

    # ชุดสุดท้ายขึ้นต้นด้วยตัวรอง
    if len(available_digits) >= 2:
        three_sets.append(right_single + available_digits[-2] + available_digits[-1])
    else:
        # ถ้าเหลือตัวเดียว → ใช้ fallback
        three_sets.append(right_single + available_digits[0] + left_single)

    return three_sets[:3]  # จำกัดแค่ 3 ชุด


# ============================================================
# 🖼️ ฟังก์ชันสร้างภาพแนวทางหวย (แก้ไขชื่อและตรรกะการวนลูป)
# ============================================================
def generate_single_lotto_images(image_path, font_path, output_dir, date_to_use,
                        count_per_template=1,
                        template_name="Default",
                        lotto_title="",            # รับชื่อหวย
                        closing_time="",           # รับเวลาปิดรับ
                        positions=None, 
                        template_data=None, # 💡 [แก้ไข] เปลี่ยนชื่อ parameter 'font_sizes' เป็น 'template_data'
                        log_callback=None, 
                        progress_callback=None, # 💡 [เพิ่ม] progress_callback
                        preview_callback=None):
    
    """
    ✅ ฟังก์ชันหลักสำหรับสร้างชุดภาพ (count_per_template) สำหรับ *1 ชื่อหวย* และ *1 Template*
    """
    
    # 💡 [แก้ไข] ดึง dict ของ font_sizes ออกมาจาก template_data
    if template_data is None:
        template_data = {} # ป้องกัน Error
    font_sizes = template_data.get("font_sizes", {}) # ดึง dict 'font_sizes' ออกมา

    # ถ้ายังไม่มีโฟลเดอร์ output → สร้างใหม่
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # โหลดภาพพื้นหลัง
    try:
        template_img = Image.open(image_path).convert("RGB")
    except Exception as e:
        if log_callback:
            log_callback(f"❌❌❌ Error: ไม่สามารถโหลดภาพเทมเพลตที่ '{image_path}': {e}")
        return # หยุดการทำงานสำหรับเทมเพลตนี้

    original_width, original_height = template_img.size

    # ถ้า OUTPUT_WIDTH หรือ OUTPUT_HEIGHT เป็น None → ใช้ขนาดเดิม
    # 💡 [แก้ไข] ตรวจสอบว่า template_data["output_width"] เป็น None หรือไม่
    width_setting = template_data.get("output_width") # (ดึงมาจาก template_data)
    height_setting = template_data.get("output_height") # (ดึงมาจาก template_data)

    width = width_setting if width_setting is not None else original_width
    height = height_setting if height_setting is not None else original_height

    # คำนวณอัตราส่วนเพื่อปรับขนาดภาพ
    # (ย้าย original_width, original_height มาไว้ที่นี่)
    original_width, original_height = template_img.size


    # ปรับอัตราส่วน scaling
    scale_x = width / original_width
    scale_y = height / original_height
    
    # 💡 [แก้ไข] เปลี่ยน ANTIALIAS เป็น LANCZOS
    resample_filter = Image.Resampling.LANCZOS
    resized_img = template_img.resize((width, height), resample_filter)

    # ปรับพิกัดทั้งหมดตามขนาดใหม่
    # 💡 [แก้ไข] ตรวจสอบว่า positions ไม่ใช่ None ก่อน
    if positions is None:
        positions = []
    scaled_positions = [(int(x*scale_x), int(y*scale_y), t) for x,y,t in positions]

    # ฟังก์ชันโหลดฟอนต์
    def load_font(path, size):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            if log_callback:
                log_callback(f"⚠️ ไม่สามารถโหลดฟอนต์ '{path}'. ใช้ฟอนต์เริ่มต้นแทน")
            return ImageFont.load_default()
            
    # โหลดฟอนต์แต่ละขนาด
    # 💡 [แก้ไข] ใช้ dict 'font_sizes' ที่เราดึงออกมา
    font_title = load_font(font_path, font_sizes.get("TITLE", FONT_SIZE_CUSTOM_TITLE))
    font_closing = load_font(font_path, font_sizes.get("CLOSING", FONT_SIZE_CLOSING_TIME))
    font_date = load_font(font_path, font_sizes.get("DATE", FONT_SIZE_DATE))
    
    # ตรวจสอบว่า Key "ONE", "TWO", "THREE", "FIVE" มีอยู่ใน dict ที่ส่งมาหรือไม่
    # (เพื่อรองรับ template_single.py ที่ไม่มีบาง Key)
    font_1_digit = load_font(font_path, font_sizes.get("ONE", FONT_SIZE_1_DIGIT))
    font_2_digits = load_font(font_path, font_sizes.get("TWO", FONT_SIZE_2_DIGITS))
    font_3_digit = load_font(font_path, font_sizes.get("THREE", FONT_SIZE_3_DIGITS))
    font_5_digits = load_font(font_path, font_sizes.get("FIVE", FONT_SIZE_5_DIGITS))
    
    used_five_digit_numbers = set()  # เก็บชุดที่ใช้แล้ว
    
    # 🆕 ฟังก์ชันวาดข้อความบนพื้นหลังมุมโค้ง
    def draw_text_with_rounded_background(
            draw, text, x_center, y_center, font,
            text_color="white", bg_color=(255, 0, 0),
            padding_x=40, padding_y=10, corner_radius=25
        ):
        """วาดข้อความพร้อมพื้นหลังสี่เหลี่ยมมุมโค้ง (ใช้สำหรับ TITLE)"""
        # 1. หาขนาดข้อความ
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 2. คำนวณขอบเขตของพื้นหลัง
        rect_left = x_center - (text_width / 2) - padding_x
        rect_top = y_center - (text_height / 2) - padding_y
        rect_right = x_center + (text_width / 2) + padding_x
        rect_bottom = y_center + (text_height / 2) + padding_y

        # 3. วาดพื้นหลังมุมโค้ง (ใช้ ImageDraw.rounded_rectangle)
        try:
            draw.rounded_rectangle(
                (rect_left, rect_top, rect_right, rect_bottom),
                radius=corner_radius,
                fill=bg_color
            )
        except AttributeError:
            # Fallback หาก ImageDraw ไม่มี rounded_rectangle (แนะนำให้อัพเดต Pillow)
            draw.rectangle((rect_left, rect_top, rect_right, rect_bottom), fill=bg_color)
            if log_callback:
                 log_callback("⚠️ เตือน: ไม่สามารถวาดมุมโค้งได้ - กรุณาอัพเดต Pillow.")

        # 4. วาดข้อความ
        draw.text(
            (x_center, y_center),
            text,
            font=font,
            fill=text_color,
            anchor="mm" # จัดกึ่งกลางข้อความ
        )

    used_five_digit_numbers = set()
    
    # 🔁 ลูปสร้างภาพทั้งหมดตามจำนวนชุด (count_per_template)
    for num_run in range(1, count_per_template + 1): # ✅ ลูปที่ถูกต้อง
        img = resized_img.copy()
        draw = ImageDraw.Draw(img)

        # สุ่มชุดตัวเลขทั้งหมด
        numbers = generate_lotto_numbers(used_five_digit_numbers)
        numbers["three_digits"] = generate_three_digit_sets(
            numbers["five_digits"], numbers["left_single"], numbers["right_single"]
        )

        top_used = bottom_used = three_used = 0
        left_single_used = False # 💡 [เพิ่ม] ตัวแปรเพื่อเช็คว่าเลข 1 ตัวแรกใช้ไปหรือยัง

        # วาดข้อความตามจุดพิกัด
        for idx, (x, y, type_or_digits) in enumerate(scaled_positions):
            current_text = ""
            current_font = font_2_digits
            text_fill_color = "white"
            stroke_fill_color = "black" # สีขอบเริ่มต้น
            bg_color_title = "black"      # สีพื้นหลัง
            corner_radius_title = 25      # ความโค้ง 25
            padding_x_title = 40          # ระยะขอบแนวนอน
            padding_y_title = 20          # ระยะขอบแนวตั้ง

            # ชื่อหวย
            if type_or_digits == "TITLE":
                current_text = lotto_title
                current_font = font_title
                
                # 🎯 เรียกใช้ฟังก์ชันใหม่เพื่อวาดพื้นหลังและข้อความ
                draw_text_with_rounded_background(
                    draw,
                    text=current_text,
                    x_center=x,
                    y_center=y,
                    font=current_font,
                    text_color="white",
                    bg_color=bg_color_title,
                    padding_x=padding_x_title,
                    padding_y=padding_y_title,
                    corner_radius=corner_radius_title
                )
                continue # ⚠️ ข้ามการวาด draw.text() ปกติ

            # ✅ เวลาเปิดรับ — ถ้าไม่มีให้ข้าม
            elif type_or_digits == "CLOSING_TIME":
                if closing_time.strip(): # 💡 ใช้ closing_time ที่ส่งเข้ามา
                    current_text = closing_time
                    current_font = font_closing
                    text_fill_color = "yellow"
                    stroke_fill_color = "red"
                else:
                    continue  # ❌ ไม่มีเวลา → ไม่วาด

            # วันที่ออก
            elif type_or_digits == "DATE":
                current_text = date_to_use
                current_font = font_date
                text_fill_color = "black"
                stroke_fill_color = "white"

            # เลข 5 หลัก
            elif type_or_digits == 5:
                current_text = numbers["five_digits"]
                current_font = font_5_digits
                text_fill_color = "red"
                stroke_fill_color = "white" # ขอบสีขาวสำหรับเลข 5 หลัก

            # เลขตัวเดียว (เด่น/รอง)
            elif type_or_digits == 1:
                # 💡 [แก้ไข] ใช้วิธีเช็คตัวแปร boolean แทน idx
                if not left_single_used:
                    current_text = numbers["left_single"]
                    left_single_used = True
                else:
                    current_text = numbers["right_single"]
                    
                current_font = font_1_digit
                text_fill_color = "black"
                stroke_fill_color = "white" # ขอบสีขาว

            # ชุดเลข 2 หลัก
            elif type_or_digits == 2:
                if top_used < len(numbers["top_pairs"]):
                    current_text = numbers["top_pairs"][top_used]; top_used += 1
                elif bottom_used < len(numbers["bottom_pairs"]):
                    current_text = numbers["bottom_pairs"][bottom_used]; bottom_used += 1
                else:
                    current_text = f"{random.randint(0,99):02d}"
                current_font = font_2_digits
                text_fill_color = "red"
                stroke_fill_color = "white" # ขอบสีขาว

            # ชุดเลข 3 หลัก
            elif type_or_digits == 3:
                if three_used < len(numbers["three_digits"]):
                    current_text = numbers["three_digits"][three_used]; three_used += 1
                else:
                    current_text = f"{random.randint(0,999):03d}"
                current_font = font_3_digit
                text_fill_color = "black"
                stroke_fill_color = "white" # ขอบสีขาว

            # วาดข้อความลงภาพ
            draw.text((x, y), current_text, font=current_font,
                      fill=text_fill_color, stroke_fill=stroke_fill_color,
                      stroke_width=6, anchor="mm")

        # แสดงใน Log และบันทึกไฟล์ภาพ
        if log_callback:
            log_callback(f"[{template_name} / {lotto_title} / ใบที่ {num_run}] 5หลัก: {numbers['five_digits']} | 3หลัก: {', '.join(numbers['three_digits'])}")
        
        # สร้างโฟลเดอร์ย่อยสำหรับแต่ละเทมเพลต
        safe_title = lotto_title.replace(" ", "_").replace("/", "-").replace(":", "-").replace(".", "-")

        # เรียกใช้ฟังก์ชัน get_safe_template_name
        safe_template_name = get_safe_template_name(template_name)

        # สร้างชื่อโฟลเดอร์ย่อยในรูปแบบ "ชื่อเทมเพลต-วันที่"

        # ทำความสะอาดวันที่สำหรับใช้ในชื่อโฟลเดอร์ (เปลี่ยน / เป็น -)
        safe_date = date_to_use.replace("/", "-").replace("\\", "-").replace(":", "-")
        
        # รวมชื่อเทมเพลตและวันที่
        folder_name = f"{safe_template_name}-{safe_date}"
        
        # สร้าง path เต็ม
        template_output_dir = os.path.join(output_dir, folder_name)
        
        # สร้างโฟลเดอร์จริง (ถ้ายังไม่มี)
        if not os.path.exists(template_output_dir):
            os.makedirs(template_output_dir, exist_ok=True)
            
        # 💡 [แก้ไข] แก้ไขชื่อไฟล์ให้ถูกต้องตามที่คุยกันไว้ (ไม่มีชื่อเทมเพลตซ้ำ)
        output_filename = f"{safe_title}_ใบที่_{num_run}.jpg"
        
        # รวม Path โฟลเดอร์ย่อย กับ ชื่อไฟล์
        output_file = os.path.join(template_output_dir, output_filename)
        
        try:
            img.save(output_file, format="JPEG", quality=95)
        except Exception as e:
            if log_callback:
                log_callback(f"❌❌❌ Error: ไม่สามารถบันทึกไฟล์ '{output_file}': {e}")
            continue # ทำงานใบถัดไปต่อ

        if preview_callback:
            preview_callback(output_file)
            
        # 💡 [เพิ่ม] อัปเดต Progress Bar ทีละ 1 เมื่อสร้างเสร็จ 1 ใบ
        if progress_callback:
            progress_callback(increment=True)

# ============================================================
# 💡 [ลบ] Class TemplateEditorWindow ทั้งหมดออกจาก main.py
# (ย้ายไปไว้ใน editor.py)
# ============================================================


# ============================================================
# 🪟 ส่วนของ GUI (โปรแกรมหลัก)
# ============================================================
class LottoGuideApp:
    """GUI สำหรับโปรแกรมสร้างใบแนวทาง"""
    def __init__(self, root):
        self.root = root
        self.root.title("Lotto Generator by D3V STUDIO")
        self.root.geometry("920x1000+-5+0")
        self.root.configure(bg=HIGHLIGHT)
        style = tb.Style(theme="darkly")

        # หัวข้อโปรแกรม
        header = tk.Label(root, text="Lotto Guide",
                          font=("BaiJamjuree-Regular", 32, "bold"),
                          bg=THEME_COLOR, fg=HIGHLIGHT)
        header.pack(pady=(10,0))

        # -----------------------
        # แสดง Template + ปุ่มเลือกทั้งหมด
        # -----------------------
        thumb_frame = tk.Frame(root, bg=THEME_COLOR)
        thumb_frame.pack(pady=10)

        # dict เก็บตัวแปร BooleanVar สำหรับแต่ละ Template
        self.template_vars = {}
        
        # ตัวแปรเก็บสถานะว่าตอนนี้เลือกทั้งหมดหรือยัง
        self.all_selected = False

        # List สำหรับเก็บ Reference ของรูปภาพ Template ทั้งหมด
        self.template_image_references = []
        
        # ฟังก์ชันสำหรับติ๊ก Template ทั้งหมด
        def toggle_select_all():
            """ฟังก์ชันเลือกทั้งหมดหรือยกเลิกทั้งหมด"""
            self.all_selected = not self.all_selected  # สลับสถานะ
            for var in self.template_vars.values():    # วนลูปทุก Template
                var.set(self.all_selected)  # ตั้งค่า Checkbox ตามสถานะ

        # ปุ่ม toggle เลือก/ยกเลิกทั้งหมด
        btn_select_all = tk.Button(
            root, 
            text="เลือกทั้งหมด", 
            font=("BaiJamjuree", 14, "bold"),
            bg="#E24800", fg="white", 
            relief="flat", bd=0,
            padx=10, pady=4, 
            cursor="hand2", 
            command=toggle_select_all
        )
        btn_select_all.pack(pady=(0,10))

        # 💡 [แก้ไข] ลบการวนลูปเปล่าๆ ออก
        # for i, temp in enumerate(TEMPLATES):
        #     f = tk.Frame(thumb_frame, bg=THEME_COLOR, padx=15)

        # สร้างกรอบแสดง Template แต่ละอัน และ Checkbox พร้อมกัน
        for i, temp in enumerate(TEMPLATES):
            # 1. สร้าง Frame (f) และจัดตำแหน่ง
            f = tk.Frame(thumb_frame, bg=THEME_COLOR, padx=15) # กรอบแต่ละ Template
            f.grid(row=0, column=i) # จัดเรียงเป็นแถวเดียว

            # 2. โหลดภาพ Thumbnail และเก็บ Reference
            try:
                img = Image.open(temp["image"])
                img.thumbnail(THUMBNAIL_SIZE) # ย่อภาพให้ขนาด Thumbnail
                photo = ImageTk.PhotoImage(img)
                self.template_image_references.append(photo) # เก็บ Reference
            except Exception:
                photo = None # ถ้าโหลดภาพไม่สำเร็จ ให้เป็น None

            # 3. แสดงภาพ
            lbl = tk.Label(f, image=photo, bg=THEME_COLOR)
            lbl.image = photo # เก็บ reference เพื่อไม่ให้ถูกลบ (ป้องกัน GC)
            lbl.pack(pady=4)

            # 4. สร้าง Checkbox และเก็บสถานะ
            var = tk.BooleanVar(value=False) # ตัวแปรเก็บสถานะติ๊ก(เริ่มต้นไม่ติ๊ก)

            # 5. เก็บตัวแปรเข้า Dictionary ก่อนใช้งาน
            self.template_vars[temp["name"]] = var # เก็บไว้ใน dict
            chk = tk.Checkbutton(
                    f, 
                    text=temp["name"], 
                    font=25, 
                    variable=var,
                    fg="white", bg=THEME_COLOR,
                    activebackground=THEME_COLOR,
                    selectcolor=THEME_COLOR
                )
            chk.pack()       
# -----------------------
# ฟอร์มกรอกข้อมูล

        # -----------------------
        # ฟอร์มกรอกข้อมูล (โค้ดนี้จะตามมาหลังลูป for จบ)
        # -----------------------
        tomorrow = datetime.now() + timedelta(days=1)
        thai_year = tomorrow.year + 543  # แปลงเป็น พ.ศ.
        thai_date = f"{tomorrow.day}/{tomorrow.month}/{str(thai_year)[-2:]}"  # รูปแบบวันที่

        form = tk.Frame(root, bg=THEME_COLOR)
        form.pack(pady=2)

        self.date_var = tk.StringVar(value=thai_date)  # วันที่ออกหวย
        self.count_var = tk.StringVar(value="1")       # จำนวนรูปต่อชุด
        self.output_path = tk.StringVar(value=DEFAULT_OUTPUT)  # โฟลเดอร์ Output

        # สร้างช่องกรอกวันที่ออกหวย
        self._add_entry(form, "วันที่ออกหวย :", self.date_var, 0)
        # สร้างช่องกรอกจำนวนรูปต่อชุด
        self._add_entry(form, "จำนวนรูปต่อชุด :", self.count_var, 1)
        # เอาช่องเลือกฟอนต์ออกแล้ว ใช้ DEFAULT_FONT ตายตัว
        self.font_path = tk.StringVar(value=DEFAULT_FONT)
        # ช่องโฟลเดอร์ Output
        self._add_entry(form, "โฟลเดอร์ Output :", self.output_path, 2, browse_dir=True)

                # ปุ่มเริ่ม
        self.start_btn = tk.Button(root, text="เริ่มสร้างภาพ",
                                   font=("BaiJamjuree-Regular", 16, "bold"),
                                   bg="#E24800", fg="white",
                                   activebackground="#FFA040",
                                   relief="flat", bd=0,
                                   padx=30, pady=8,
                                   cursor="hand2",
                                   command=self.start_generate)
        self.start_btn.pack(pady=15)

        # 💡 [ลบ] ปุ่ม "แก้ไขตำแหน่ง" ออกจาก main.py
        # self.edit_btn = tk.Button(...)
        # self.edit_btn.pack(...)

        # แถบ Progress
        self.progress = ttk.Progressbar(root, orient="horizontal", length=700, mode="determinate")
        self.progress.pack(pady=(15,5))

        # สถานะการทำงาน
        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(
            root,
            textvariable=self.status_var,
            font=("BaiJamjuree", 12),
            bg=THEME_COLOR,
            fg="white"
        )
        self.status_label.pack(pady=(5, 5))

        # ส่วนแสดง Preview ล่าสุด
        footer = tk.Label(root, text="©D3V 2025", font=("Arial", 9),
                          bg=THEME_COLOR, fg="#777")
        footer.pack(pady=(5,0))
        self.preview_label = ctk.CTkLabel(root, text="(Preview)", width=120, height=220)
        self.preview_label.pack(pady=(6,10))

    def preview_callback(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((120, 220))
            photo = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            print("Preview error:", e)
            self.preview_label.configure(text="Preview error", image=None)

    # -----------------------
    # ฟังก์ชันย่อยของ GUI
    # -----------------------
    def _add_entry(self, parent, label, var, row, browse=False, browse_dir=False):
        """สร้างช่องกรอกข้อมูลในฟอร์ม"""
        tk.Label(parent, text=label, font=("BaiJamjuree-Bold.ttf", 11),
                 bg=THEME_COLOR, fg="white").grid(row=row, column=0, sticky="e", padx=10, pady=6)
        entry = tk.Entry(parent, textvariable=var, font=("BaiJamjuree-Bold.ttf", 10),
                         width=40, relief="flat",
                         highlightthickness=1, highlightbackground="#444",
                         bg="#2A2A2A", fg="white", insertbackground="white")
        entry.grid(row=row, column=1, pady=6, sticky="w")

        # ปุ่มเลือกไฟล์หรือโฟลเดอร์
        if browse:
            tk.Button(parent, text="เลือกไฟล์", command=lambda: self._browse_file(var),
                      bg="#E24800", fg="white", relief="flat", cursor="hand2", width=8, padx=4, pady=2).grid(row=row, column=2, padx=10)
        elif browse_dir:
            tk.Button(parent, text="เลือกโฟลเดอร์", command=lambda: self._browse_dir(var),
                      bg="#E24800", relief="flat", cursor="hand2", width=8, padx=4, pady=2).grid(row=row, column=2, padx=10)

    def _browse_file(self, var):
        """เลือกไฟล์ฟอนต์"""
        p = filedialog.askopenfilename(title="เลือกไฟล์", filetypes=[("Font files", "*.ttf *.otf")])
        if p: var.set(p)

    def _browse_dir(self, var):
        """เลือกโฟลเดอร์ Output"""
        d = filedialog.askdirectory(title="เลือกโฟลเดอร์")
        if d: var.set(d)

    # 💡 [ลบ] ฟังก์ชัน open_template_editor ออกจาก main.py
    # def open_template_editor(self):
    #     ...

    def start_generate(self):
        """เริ่มสร้างภาพ"""
        selected = [name for name,var in self.template_vars.items() if var.get()]
        if not selected:
            # ❌ เดิมใช้ messagebox → เปลี่ยนเป็นแสดงสถานะแทน
            self.status_var.set("⚠️ กรุณาเลือกใบแนวทางอย่างน้อย 1 ใบ")
            self.root.after(5000, lambda: self.status_var.set(""))  # ล้างข้อความหลัง 5 วินาที
            return

        # 💡 คำนวณจำนวนงานทั้งหมด (Template x ชื่อหวย x จำนวนชุด)
        count_per_template = int(self.count_var.get()) if self.count_var.get().isdigit() else 1
        self.total_tasks = len(selected) * OUTPUT_COUNT * count_per_template # 🆕 ตั้งค่า total_tasks
        self.current_task = 0 # 🆕 ตั้งค่าตัวนับ
        self.progress['maximum'] = self.total_tasks # 🆕 กำหนดค่าสูงสุดของ Progress Bar

        self.start_btn.config(state="disabled")
        self.progress['value'] = 0
        thread = threading.Thread(target=self._run_worker, daemon=True)
        thread.start()

    def _run_worker(self):
        """ประมวลผลใน Thread แยก"""
        try:
            selected_templates = [name for name, var in self.template_vars.items() if var.get()]
            count_per_template = int(self.count_var.get()) if self.count_var.get().isdigit() else 1

            # 1. 🆕 วนลูปตามชื่อหวยทั้งหมด (CUSTOM_TITLES)
            for i, (lotto_title, closing_time) in enumerate(zip(CUSTOM_TITLES, CLOSING_TIME)):
                
                # 2. 🆕 วนลูปตาม Template ที่ผู้ใช้เลือก (selected_templates)
                for template_name in selected_templates:
                    template_data = next((t for t in TEMPLATES if t["name"] == template_name), None)

                    if template_data is None:
                        self._log_cb(f"⚠️ ข้ามการสร้างภาพ: ไม่พบข้อมูลเทมเพลต '{template_name}'")
                        # 💡 [แก้ไข] อัปเดต progress bar สำหรับงานที่ข้ามไป
                        self._progress_cb(increment=count_per_template) 
                        continue
                    
                    # 💡ตรรกะการเลือก Positions
                    default_positions = template_data.get("positions", []) # ใช้ .get ป้องกัน Key Error
                    custom_positions = load_custom_positions(template_name) # โหลดจาก .json
                    
                    # ถ้ามีไฟล์ .json ให้ใช้, ถ้าไม่มี ให้ใช้ค่า default
                    positions_to_use = custom_positions if custom_positions else default_positions
                        
                    # 💡 [แก้ไข] ลบการเรียก generate_single_lotto_images ที่ซ้ำซ้อนออก
                    # เหลือแค่การเรียกเดียวที่ใช้ positions_to_use
                    generate_single_lotto_images( 
                        image_path=template_data["image"],
                        font_path=self.font_path.get(),
                        output_dir=self.output_path.get(),
                        date_to_use=self.date_var.get(),
                        count_per_template=count_per_template,
                        template_name=template_name,
                        lotto_title=lotto_title,
                        closing_time=closing_time,
                        positions=positions_to_use, # 💡 ส่ง positions ที่เลือกแล้วเข้าไป
                        template_data=template_data, # 💡 [แก้ไข] ส่ง dict ทั้งก้อนเข้าไป
                        log_callback=self._log_cb,
                        progress_callback=self._progress_cb, # 💡 [เพิ่ม] ส่ง callback progress
                        preview_callback=self._preview_cb
                    )
                    
                    # 💡 [ลบ] ลบการอัปเดต Progress Bar ที่ผิดพลาดออกจากที่นี่
                    # (ย้ายเข้าไปใน generate_single_lotto_images แล้ว)
                    # self.current_task += count_per_template 
                    # self.root.after(0, lambda: self._progress_cb(self.current_task))


            # ✅ แสดงข้อความสถานะแทน popup
            self.root.after(0, lambda: self.status_var.set("✅ สร้างภาพทั้งหมดเสร็จเรียบร้อย"))
            self.root.after(10000, lambda: self.status_var.set(""))  # ล้างข้อความหลัง 10 วินาที
            
            # 💡 [แก้ไข] รีเซ็ต Progress Bar เมื่อเสร็จ
            self.root.after(0, lambda: self._progress_cb(value=0)) # ใช้ value=0


        except Exception as e:
            self.root.after(0, lambda e=e: self.status_var.set(f"❌ เกิดข้อผิดพลาด: {e}"))
            self.root.after(10000, lambda: self.status_var.set(""))  # ล้างข้อความหลัง 10 วินาที
        finally:
            self.root.after(0, lambda: self.start_btn.config(state="normal"))

    # 💡 [แก้ไข] แก้ไข _progress_cb และ _log_cb ให้รองรับการอัปเดตจาก generate_...
    def _progress_cb(self, value=None, increment=False):
        """อัปเดต Progress bar (รองรับการเพิ่มทีละ 1)"""
        if increment:
            # 💡 [แก้ไข] ต้องอ่านค่า value จากตัว progress bar โดยตรง
            current_val = self.progress['value']
            self.root.after(0, lambda: self.progress.configure(value=current_val + 1))
        elif value is not None:
            self.root.after(0, lambda: self.progress.configure(value=value))

    def _log_cb(self, text):
        """แสดงข้อความ Log"""
        print(text)
        # อัปเดต status label ไปด้วยเลย
        self.root.after(0, lambda: self.status_var.set(text))

    def _preview_cb(self, path):
        """อัปเดตรูป Preview"""
        def do_preview():
            try:
                img = Image.open(path); img.thumbnail((120,220))
                photo = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=photo, text=""); self.preview_label.image = photo
            except Exception:
                self.preview_label.configure(text="Preview error")
        self.root.after(0, do_preview)

# ============================================================
# 🚀 เริ่มโปรแกรม
# ============================================================
if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = LottoGuideApp(root)
    # customtkinter widget (ใช้ root เดียวกันได้)
    # 💡 [ลบ] ปุ่มกับสวิตช์ทดสอบของ customtkinter ออก
    # btn = CTkButton(master=root, text="กดปุ่มจาก CustomTkinter")
    # btn.pack(pady=10)

    # switch = CTkSwitch(master=root, text="เปิด / ปิด")
    # switch.pack(pady=10)
    root.mainloop()