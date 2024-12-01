import ctypes
import pygame
import os
import win32gui
import win32con

class WallpaperManager:
	def __init__(self):
		self.is_running = False

	def start_image_animation(self, folder_path, frame_rate=30):
		print(f"start_image_animation called with folder: {folder_path}")

		if self.is_running:
			print("アニメーションはすでに実行中です")
			return False

		if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
			print("フォルダが見つかりません")
			return False

		self.is_running = True
		self._play_images(folder_path, frame_rate)
		return True

	def stop_animation(self):
		self.is_running = False
		pygame.quit()
		print("アニメーションを停止しました")
		self._restore_wallpaper()

	def _play_images(self, folder_path, frame_rate):
		try:
			pygame.init()

			# DPI認識を有効にする
			ctypes.windll.user32.SetProcessDPIAware()

			# スクリーンサイズを取得（DPIスケーリングを考慮）
			user32 = ctypes.windll.user32
			screen_width = user32.GetSystemMetrics(0)
			screen_height = user32.GetSystemMetrics(1)

			screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
			clock = pygame.time.Clock()

			workerw = self._get_workerw()
			window_info = pygame.display.get_wm_info()
			hwnd = window_info['window']

			# ウィンドウスタイルを取得して修正
			style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
			style &= ~(win32con.WS_OVERLAPPEDWINDOW)
			win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

			# ウィンドウをデスクトップ全体に配置
			win32gui.SetWindowPos(
				hwnd,
				win32con.HWND_TOPMOST,
				0,
				0,
				screen_width,
				screen_height,
				win32con.SWP_NOOWNERZORDER | win32con.SWP_FRAMECHANGED
			)

			# PygameウィンドウをWorkerWの子ウィンドウに設定
			ctypes.windll.user32.SetParent(hwnd, workerw)

			# 処理済みのファイルを追跡するセット
			processed_files = set()

			time_delay_ms = 10

			while self.is_running:
				# フォルダ内の画像を取得しソート（新しい画像を検出）
				all_files = sorted(
					[os.path.join(folder_path, f) for f in os.listdir(folder_path)
					if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
				)

				# 新しい画像のみをリストアップ
				new_files = [f for f in all_files if f not in processed_files]

				# 新しい画像を処理
				for image_file in new_files:
					if not self.is_running:
						break

					# 画像をロードして画面サイズに合わせる
					image = pygame.image.load(image_file)
					image = pygame.transform.smoothscale(image, (screen_width, screen_height))

					# 画面に描画して更新
					screen.blit(image, (0, 0))
					pygame.display.update()

					# フレームレートに応じて待機
					clock.tick(frame_rate)

					pygame.time.delay(time_delay_ms)

					# 画像を削除
					try:
						os.remove(image_file)
						print(f"画像を削除しました: {image_file}")
						processed_files.add(image_file)  # 処理済みリストに追加
					except Exception as e:
						print(f"画像の削除中にエラーが発生しました: {image_file}, {str(e)}")

					# Pygameイベント処理
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							self.is_running = False

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
			default_wallpaper_path = "C:\\Windows\\Web\\Wallpaper\\Windows\\img0.jpg"
			if os.path.exists(default_wallpaper_path):
				ctypes.windll.user32.SystemParametersInfoW(
					20,
					0,
					default_wallpaper_path,
					3
				)
				print("元の壁紙に復元しました")
			else:
				print("デフォルトの壁紙パスが見つかりません")
		except Exception as e:
			print("壁紙の復元中にエラーが発生しました:", str(e))


# 使用例
if __name__ == "__main__":
	current_dir = os.path.dirname(os.path.abspath(__file__))
	image_folder_path = os.path.join(current_dir, "images")

	if not os.path.exists(image_folder_path):
		print(f"画像フォルダが見つかりません: {image_folder_path}")
	else:
		manager = WallpaperManager()
		try:
			frame_rate = 15
			manager.start_image_animation(image_folder_path, frame_rate)
		except KeyboardInterrupt:
			manager.stop_animation()