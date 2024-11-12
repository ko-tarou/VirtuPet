import ctypes
import ctypes.wintypes
import win32gui
import pygame
import pyautogui
import win32con  # 追加
from smooth_movement import smooth_move

# ディスプレイ解像度の自動取得
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# デスクトップの背景ウィンドウ（Progmanウィンドウ）を取得してWorkerWウィンドウを作成
def get_workerw():
    # Progmanウィンドウのメッセージを送信して新しいWorkerWウィンドウを作成
    win32gui.SendMessageTimeout(
        win32gui.FindWindow("Progman", None),
        0x052C,
        0,
        0,
        win32con.SMTO_NORMAL,
        1000
    )
    # WorkerWウィンドウを取得
    workerw = None
    def enum_windows_callback(hwnd, _):
        nonlocal workerw  # workerw を関数外で使用するために nonlocal を使う
        class_name = win32gui.GetClassName(hwnd)
        if class_name == "WorkerW":
            workerw = hwnd
    win32gui.EnumWindows(enum_windows_callback, None)
    return workerw

# Pygame初期設定
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()

# アニメーションする画像を読み込む
background = pygame.image.load("../static/images/background.jpg")
animal_image = pygame.image.load("../static/images/animal_sprite.png")
animal_rect = animal_image.get_rect()
background = pygame.transform.scale(background, (screen_width, screen_height))

# 初期位置
x, y = 100, 100

# WorkerWウィンドウに対して描画
workerw = get_workerw()

# pygame.display.get_wm_info() を使用してウィンドウハンドルを取得
window_info = pygame.display.get_wm_info()
hwnd = window_info['window']

# SetParent を使って WorkerW ウィンドウに親として設定
ctypes.windll.user32.SetParent(hwnd, workerw)

# メインループ
while True:
    # マウスの位置を取得
    target_x, target_y = pyautogui.position()
    x, y = smooth_move(x, y, target_x, target_y)

    # 背景画像を描画
    screen.blit(background, (0, 0))

    # 動物の画像を描画
    animal_rect.topleft = (x, y)
    screen.blit(animal_image, animal_rect)
    
    # 更新
    pygame.display.update()
    clock.tick(60)

    # 終了イベントのチェック
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()