from animal_animation import AnimalAnimation
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
		self.animal_animation = AnimalAnimation(speed=5)  # アニメーションロジックを持つクラスをインスタンス化

	def start_animation(self, size_multiplier):
		print(f"start_animation called with size: {size_multiplier}")
		with self.lock:
			if self.is_animating:
				print("アニメーションはすでに実行中です")
				return False

			if self.animation_thread and self.animation_thread.is_alive():
				print("古いスレッドを停止します")
				self.stop_animation()

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
				pygame.event.post(pygame.event.Event(pygame.QUIT))
				if self.animation_thread:
					self.animation_thread.join()
				pygame.quit()
				print("Animation stopped and resources released.")
				return True
			print("アニメーションは実行されていません")
			return False

	def _run_animation(self, size_multiplier):
		try:
			pygame.init()

			user32 = ctypes.windll.user32
			screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

			screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
			clock = pygame.time.Clock()

			workerw = self._get_workerw()
			window_info = pygame.display.get_wm_info()
			hwnd = window_info['window']
			ctypes.windll.user32.SetParent(hwnd, workerw)

			background_path = os.path.abspath("../static/images/background.jpg")
			animal_path = os.path.abspath("../static/images/animal_sprite.png")

			if not os.path.exists(background_path) or not os.path.exists(animal_path):
				print("背景または動物画像が見つかりません")
				self.is_animating = False
				return

			background = pygame.image.load(background_path)
			animal_image = pygame.image.load(animal_path)

			scaled_animal_image = pygame.transform.scale(
				animal_image,
				(int(animal_image.get_width() * size_multiplier),
				int(animal_image.get_height() * size_multiplier))
			)
			background = pygame.transform.scale(background, (screen_width, screen_height))
			animal_rect = scaled_animal_image.get_rect()

			while self.is_animating:
				# マウスの位置を取得
				target_x, target_y = pyautogui.position()

				# アニメーションロジックを使用して新しい位置を計算
				x, y = self.animal_animation.update_position(target_x, target_y)

				# 背景と動物を描画
				screen.blit(background, (0, 0))
				animal_rect.topleft = (x, y)
				screen.blit(scaled_animal_image, animal_rect)

				pygame.display.update()
				clock.tick(60)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.is_animating = False

			pygame.quit()
			print("Pygame animation stopped")
		except Exception as e:
			print("アニメーションの実行中にエラーが発生しました:", str(e))
			self.is_animating = False

	def _get_workerw(self):
		progman = win32gui.FindWindow("Progman", None)
		win32gui.SendMessageTimeout(
			progman,
			0x052C,
			0,
			0,
			win32con.SMTO_NORMAL,
			1000
		)

		workerw = None
		def enum_windows_callback(hwnd, _):
			nonlocal workerw
			if win32gui.GetClassName(hwnd) == "WorkerW":
				workerw = hwnd

		win32gui.EnumWindows(enum_windows_callback, None)
		if not workerw:
			print("WorkerWウィンドウが見つかりませんでした")
		return workerw
