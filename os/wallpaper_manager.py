import pygame
import threading
import time

class WallpaperManager:
    def __init__(self):
        pygame.init()
        self.animal_image = pygame.image.load("../static/images/animal_sprite.png")
        self.is_animating = False
        self.animation_thread = None

    def start_animation(self, size):
        # アニメーションが既に実行中でない場合のみ開始
        if not self.is_animating:
            self.is_animating = True
            # 画像をスケール
            self.scaled_animal_image = pygame.transform.scale(
                self.animal_image,
                (int(self.animal_image.get_width() * size), int(self.animal_image.get_height() * size))
            )
            # 別スレッドでアニメーションを開始
            self.animation_thread = threading.Thread(target=self.animate)
            self.animation_thread.start()

    def stop_animation(self):
        # アニメーションを停止
        self.is_animating = False
        if self.animation_thread is not None:
            self.animation_thread.join()  # スレッドが終了するまで待つ
            self.animation_thread = None

    def animate(self):
        # Pygameでアニメーションを描画する処理
        screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        clock = pygame.time.Clock()
        x, y = 100, 100

        while self.is_animating:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_animating = False
                    break

            # 画面をクリアして動物を描画
            screen.fill((0, 0, 0))  # 黒でクリア
            screen.blit(self.scaled_animal_image, (x, y))
            pygame.display.update()
            clock.tick(60)
        
        # アニメーションを停止したら画面を閉じる
        pygame.quit()
