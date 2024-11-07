import os
import pyautogui
from PIL import Image
import ctypes
import time

# DPIスケールの取得
def get_scale_factor():
    hdc = ctypes.windll.user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
    ctypes.windll.user32.ReleaseDC(0, hdc)
    return dpi / 96  # 96 DPI が通常のスケール (100%)

# 壁紙の変更に使用する関数（Windows API を利用）
def set_wallpaper(image_path):
    # SPI_SETDESKWALLPAPER を使って壁紙を変更
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

# ベースとなる背景画像のパス
base_wallpaper_path = "../../public/base.jpg"  # 基本となる壁紙画像
animal_image_path = "../../public/kani.png"  # 動物の画像 (PNG形式)

# 動的なデスクトップ背景の更新
def update_wallpaper():
    # 画面サイズを取得
    screen_width, screen_height = pyautogui.size()

    # スケールファクターを取得
    scale_factor = get_scale_factor()

    while True:
        # ベースの壁紙を読み込む
        base_wallpaper = Image.open(base_wallpaper_path).convert("RGBA")
        
        # 動物の画像を読み込む
        animal_image = Image.open(animal_image_path).convert("RGBA")

        # 画像のサイズを調整する（ここでは幅200ピクセル、高さ200ピクセルに設定）
        new_size = (200, 200)  # 新しいサイズ（幅, 高さ）
        animal_image = animal_image.resize(new_size, Image.LANCZOS)

        # リサイズ後の画像の幅と高さを取得
        animal_width, animal_height = animal_image.size

        # マウスの現在位置を取得し、スケールファクターで補正（過剰補正を防ぐため、1回のみ適用）
        mouse_x, mouse_y = pyautogui.position()
        if scale_factor != 1.0:
            corrected_mouse_x = mouse_x / scale_factor
            corrected_mouse_y = mouse_y / scale_factor
        else:
            corrected_mouse_x = mouse_x
            corrected_mouse_y = mouse_y
        
        corrected_mouse_x /= 4
        corrected_mouse_y /= 4

        # マウス位置に動物の画像の中心を合わせるための位置を計算
        # 画像が画面からはみ出さないように制限 (画面サイズの半分に制限)
        position_x = max(0, min((screen_width // 4) - animal_width, corrected_mouse_x - animal_width // 2 + 150))
        position_y = max(0, min((screen_height // 4) - animal_height, corrected_mouse_y - animal_height // 2))

        # 背景に動物の画像を合成するための透明なキャンバスを作成
        canvas = Image.new("RGBA", base_wallpaper.size, (255, 255, 255, 0))

        # キャンバスに動物の画像を貼り付ける
        canvas.paste(animal_image, (int(position_x), int(position_y)), animal_image)

        # ベースの壁紙とキャンバス（動物の画像）を合成
        combined_image = Image.alpha_composite(base_wallpaper, canvas)

        # 一時的なファイルとして保存
        temp_wallpaper_path = "C:/Users/tkota/AppData/Local/Temp/temp_wallpaper.png"
        combined_image.save(temp_wallpaper_path, format="PNG")

        # 壁紙として設定
        set_wallpaper(temp_wallpaper_path)

        # 更新頻度を設定（0.1秒間隔で更新）
        time.sleep(0.0001)

# 壁紙の更新を開始
try:
    update_wallpaper()
except KeyboardInterrupt:
    print("終了しました")