import ctypes
import pygame
import threading
import cv2
import os
import pyautogui
import win32gui
import win32con

class WallpaperManager:
	def __init__(self):
		self.is_running = False
		self.lock = threading.Lock()
		self.thread = None

	def start_animation(self, size_multiplier, video_path):
		print(f"start_animation called with size: {size_multiplier}")
		with self.lock:
			if self.is_running:
				print("アニメーションはすでに実行中です")
				return False

			if not os.path.exists(video_path):
				print("動画ファイルが見つかりません")
				return False

			self.is_running = True
			self.thread = threading.Thread(
				target=self._play_video,
				args=(size_multiplier, video_path),
				daemon=True
			)
			self.thread.start()
			print("動画の再生を開始しました")
			return True

	def stop_animation(self):
		with self.lock:
			if self.is_running:
				self.is_running = False
				pygame.event.post(pygame.event.Event(pygame.QUIT))
				if self.thread:
					self.thread.join()
				pygame.quit()
				print("アニメーションを停止しました")

				# 壁紙を元に戻す
				self._restore_wallpaper()
				return True
			print("アニメーションは実行されていません")
			return False

	def _play_video(self, size_multiplier, video_path):
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

			cap = cv2.VideoCapture(video_path)

			if not cap.isOpened():
				print("動画を読み込めませんでした")
				self.is_running = False
				return

			ret, frame = cap.read()
			if not ret:
				print("動画の最初のフレームを取得できませんでした")
				self.is_running = False
				return

			while self.is_running:
				ret, frame = cap.read()
				if not ret:
					# 動画をループさせる
					cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
					ret, frame = cap.read()
					if not ret:
						break

				# OpenCVのフレームをPygameに変換
				frame = cv2.resize(frame, (screen_width, screen_height))
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				pygame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

				screen.blit(pygame_surface, (0, 0))
				pygame.display.update()
				clock.tick(30)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.is_running = False

			cap.release()
			pygame.quit()
			print("Pygame animation stopped")
		except Exception as e:
			print("アニメーションの実行中にエラーが発生しました:", str(e))
			self.is_running = False

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

	def _restore_wallpaper(self):
		try:
			# デフォルトの壁紙パス (変更が必要な場合は適宜修正)
			default_wallpaper_path = "C:\\Windows\\Web\\Wallpaper\\Windows\\img0.jpg"
			
			if os.path.exists(default_wallpaper_path):
				# Windows APIを使って壁紙を再設定
				ctypes.windll.user32.SystemParametersInfoW(
					20,  # SPI_SETDESKWALLPAPER
					0,
					default_wallpaper_path,
					3   # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
				)
				print("元の壁紙に復元しました")
			else:
				print("デフォルトの壁紙パスが見つかりません")
		except Exception as e:
			print("壁紙の復元中にエラーが発生しました:", str(e))

# 使用例
if __name__ == "__main__":
	manager = WallpaperManager()
	video_path = "../static/images/test.mp4"  # 動画ファイルのパス
	size_multiplier = 1.0  # 動物画像サイズの倍率
	manager.start_animation(size_multiplier, video_path)

	# 終了するには manager.stop_animation() を呼び出してください。
