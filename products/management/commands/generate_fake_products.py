import os
from django.core.management.base import BaseCommand
import random
from products.models import Product,ProductImage
from pathlib import Path
from django.core.files import File
from django.db import transaction





class Command(BaseCommand):
    help = 'Generate fake products data'

    # 類別與名稱模板對應
    category_names = {
        1: "相機",
        2: "電腦",
        3: "手機",
        4: "平板",
        5: "藍芽耳機",
        6: "滑鼠",
        7: "鍵盤",
        8: "SSD",
        9: "螢幕",
        10: "智慧手錶",
    }

    category_images = {
        1: 'camera_lens_set.png',   # 相機
        2: 'computer_laptop.png',  # 電腦
        3: 'smartphone.png',   # 手機
        4: 'computer_tablet.png',   # 平板
        5: 'music_earphone_true_wireless_case.png',    # 藍芽耳機
        6: 'game_gaming_mouse.png',     # 滑鼠
        7: 'computer_keyboard_black.png',     # 鍵盤
        8: 'computer_ssd.png',    # SSD
        9: 'tv_screen_black.png',   # 螢幕
        10: 'sports_katsudouryoukei.png',  # 智慧手錶
    }

    # def add_arguments(self, parser):
    #     parser.add_argument('--file', type=str, help='File to scan')

    def handle(self, *args, **kwargs):
        # 建立虛擬資料
        BASE_DIR = Path(__file__).resolve().parent
        image_dir = Path.joinpath(BASE_DIR,"sample_images")
        try:
            with transaction.atomic():
                for category in range(1, 11):
                    for _ in range(10):
                        product = Product.objects.create(
                            merchant_id=2,
                            name=self.generate_product_name(category),
                            description=self.generate_description(category),
                            price=f"{self.generate_price(category):.2f}",
                            category_id=category,
                            inventory=50
                        )

                        # 隨機選一張圖當作產品圖片
                        image_path = Path.joinpath(image_dir,self.category_images[category])
                        with open(image_path, 'rb') as f:
                            ProductImage.objects.create(
                                product=product,
                                image=File(f, name=os.path.basename(image_path)),
                                order=0,
                            )
                        print(f"product created:{product.name}")
        except Exception as e:
            print(f'Exception:{e}')
        

    # 隨機生成虛擬品牌與型號
    def generate_product_name(self,category):
        prefix = random.choice(["Zeta", "Neo", "Omni", "Astro", "Vertex", "Lumo", "Hyper", "Cyra", "Nova", "Orbi"])
        model = f"{random.choice(['X', 'S', 'T', 'M'])}{random.randint(100,999)}"
        return f"{prefix} {self.category_names[category]} {model}"

    # 隨機生成說明文字
    def generate_description(self,category):
        phrases = [
            "擁有高效能處理器與現代化設計",
            "搭配先進的顯示技術與輕巧外型",
            "支援長效電池與快速充電",
            "專為專業使用者設計，兼具穩定與效率",
            "具備高解析度與卓越的使用體驗",
            "內建最新作業系統，提供流暢操作",
            "強化連接能力與多樣擴充性",
        ]
        return f"{self.category_names[category]}裝置，{random.choice(phrases)}。"

    # 隨機價格產生器（根據類別調整範圍）
    def generate_price(self,category):
        ranges = {
            1: (5000, 30000),   # 相機
            2: (15000, 60000),  # 電腦
            3: (8000, 40000),   # 手機
            4: (7000, 30000),   # 平板
            5: (800, 10000),    # 藍芽耳機
            6: (300, 5000),     # 滑鼠
            7: (500, 6000),     # 鍵盤
            8: (1000, 8000),    # SSD
            9: (3000, 20000),   # 螢幕
            10: (2000, 15000),  # 智慧手錶
        }
        return round(random.uniform(*ranges[category]), 0)