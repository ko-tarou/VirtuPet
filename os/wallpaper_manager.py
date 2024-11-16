import ctypes
import ctypes.wintypes
import pygame
import threading
import os
import pyautogui
import win32gui
import win32con

class WallpaperManager:
    def __init__(self):
        self.is_animating = False
        self.lock = threading.Lock()
        self.animation_thread = None

    def start_animation(self, size_multiplier):
        print(f"start_animation called with size: {size_multiplier}")  # デバッグ用ログ
        with self.lock:
            if not self.is_animating:
                self.is_animating = True
                try:
                    self.animation_thread = threading.Thread(
                        target=self._run_animation,
                        args=(size_multiplier,),
                        daemon=True
                    )
                    self.animation_thread.start()
                    print(f"Animation started with size: {size_multiplier}")
                    return True
                except Exception as e:
                    print("アニメーションの開始に失敗しました:", str(e))
                    self.is_animating = False
                    return False

    def stop_animation(self):
        with self.lock:
            if self.is_animating:
                self.is_animating = False
                pygame.quit()
                print("Animation stopped.")
                return True
            return False

    def _run_animation(self, size_multiplier):
        try:
            pygame.init()

            # ディスプレイ解像度を取得
            user32 = ctypes.windll.user32
            screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

            # Pygameウィンドウの初期化
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
            clock = pygame.time.Clock()

            # WorkerWウィンドウを取得して背景に設定
            workerw = self._get_workerw()
            window_info = pygame.display.get_wm_info()
            hwnd = window_info['window']
            ctypes.windll.user32.SetParent(hwnd, workerw)

            # 背景画像と動物画像を読み込む
            background_path = os.path.abspath("../static/images/background.jpg")
            animal_path = os.path.abspath("../static/images/animal_sprite.png")

            if not os.path.exists(background_path) or not os.path.exists(animal_path):
                print("背景または動物画像が見つかりません")
                self.is_animating = False
                return

            background = pygame.image.load(background_path)
            animal_image = pygame.image.load(animal_path)

            # 画像サイズを調整
            scaled_animal_image = pygame.transform.scale(
                animal_image,
                (int(animal_image.get_width() * size_multiplier),
                 int(animal_image.get_height() * size_multiplier))
            )
            background = pygame.transform.scale(background, (screen_width, screen_height))
            animal_rect = scaled_animal_image.get_rect()

            # 初期位置
            x, y = 100, 100

            # メインループ
            while self.is_animating:
                # マウスの位置を取得
                target_x, target_y = pyautogui.position()
                x, y = self._smooth_move(x, y, target_x, target_y)

                # 背景画像を描画
                screen.blit(background, (0, 0))

                # 動物画像を描画
                animal_rect.topleft = (x, y)
                screen.blit(scaled_animal_image, animal_rect)

                # 更新
                pygame.display.update()
                clock.tick(60)

                # イベント処理
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_animating = False

            pygame.quit()
            print("Pygame animation stopped")
        except Exception as e:
            print("アニメーションの実行中にエラーが発生しました:", str(e))
            self.is_animating = False

    def _get_workerw(self):
        # Progmanウィンドウのメッセージを送信してWorkerWウィンドウを作成
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
            nonlocal workerw
            class_name = win32gui.GetClassName(hwnd)
            if class_name == "WorkerW":
                workerw = hwnd

        win32gui.EnumWindows(enum_windows_callback, None)
        return workerw

    def _smooth_move(self, x, y, target_x, target_y, speed=5):
        # 動物の位置を滑らかに移動
        dx = target_x - x
        dy = target_y - y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < speed:
            return target_x, target_y
        x += speed * dx / distance
        y += speed * dy / distance
        return x, y
