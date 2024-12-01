import os
import pygame
import time

IMAGE_DIR = "images"  # サーバーが画像を保存するディレクトリ

# Pygame の初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))  # ウィンドウサイズを設定
pygame.display.set_caption("Image Viewer")

def get_latest_image():
	"""画像ディレクトリから最新の画像ファイルを取得する"""
	files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")]
	if not files:
		return None
	files.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIR, x)))
	return os.path.join(IMAGE_DIR, files[-1])

def main():
	clock = pygame.time.Clock()
	last_displayed = None

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return

		# 最新の画像を取得
		latest_image = get_latest_image()
		if latest_image and latest_image != last_displayed:
			# 画像を読み込み
			image = pygame.image.load(latest_image)
			image = pygame.transform.scale(image, (800, 600))  # ウィンドウサイズに合わせる
			screen.blit(image, (0, 0))
			pygame.display.flip()
			last_displayed = latest_image

		clock.tick(30)  # 30FPSに制限

if __name__ == "__main__":
	if not os.path.exists(IMAGE_DIR):
		print(f"Image directory '{IMAGE_DIR}' does not exist. Please run the server first.")
	else:
		main()
