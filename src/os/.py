import ctypes
import os

def reset_to_default_wallpaper():
    default_wallpaper = r"C:\Windows\Web\Wallpaper\Windows\img0.jpg"
    ctypes.windll.user32.SystemParametersInfoW(20, 0, default_wallpaper, 3)

# デフォルト壁紙に戻す
reset_to_default_wallpaper()
