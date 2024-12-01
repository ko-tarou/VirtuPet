from quart import Quart, request, jsonify
from quart_cors import cors
from test import WallpaperManager
import json
import os
import logging

# 設定ファイルのパス
SETTINGS_FILE = "settings.json"

# ログ設定
logging.basicConfig(level=logging.INFO)

# サーバー初期化
app = Quart(__name__)
app = cors(app, allow_origin="http://localhost:3000")  # フロントエンドのオリジンを許可
wallpaper_manager = WallpaperManager()

# 動物の表示設定を保持する変数
animal_settings = {
	"is_visible": True,
	"size": 1.0,  # 初期値
	"video_path": "../static/images/test.mp4"  # デフォルトの動画パス
}

# 設定をファイルに保存する関数
def save_settings():
	try:
		with open(SETTINGS_FILE, "w") as file:
			json.dump(animal_settings, file)
		logging.info("設定を保存しました: %s", animal_settings)
	except Exception as e:
		logging.error("設定の保存に失敗しました: %s", str(e))

# 設定をファイルから読み込む関数
def load_settings():
	global animal_settings
	if os.path.exists(SETTINGS_FILE):
		try:
			with open(SETTINGS_FILE, "r") as file:
				animal_settings = json.load(file)
			logging.info("設定を読み込みました: %s", animal_settings)
		except Exception as e:
			logging.error("設定の読み込みに失敗しました: %s", str(e))

# 設定取得エンドポイント
@app.route('/get_animal_settings', methods=['GET'])
async def get_animal_settings():
	return jsonify(animal_settings)


@app.route('/set_animal_settings', methods=['POST'])
async def set_animal_settings():
	try:
		data = await request.json
		logging.info("リクエストデータを受信: %s", data)

		if "is_visible" in data:
			animal_settings["is_visible"] = bool(data["is_visible"])

		if "size" in data:
			size = float(data["size"])
			if not (0.5 <= size <= 3.0):  # サイズ範囲をチェック
				logging.warning("無効なサイズ指定: %s", size)
				return jsonify({"status": "error", "message": "サイズは0.5～3.0の範囲内で指定してください"}), 400
			animal_settings["size"] = size

		# アニメーションの開始/停止
		if animal_settings["is_visible"]:
			if not wallpaper_manager.is_running:
				# imagesフォルダのパスを取得
				current_dir = os.path.dirname(os.path.abspath(__file__))
				image_folder_path = os.path.join(current_dir, "images")

				if not os.path.exists(image_folder_path):
					logging.error("画像フォルダが見つかりません: %s", image_folder_path)
					return jsonify({"status": "error", "message": "画像フォルダが存在しません"}), 500

				# アニメーションを開始
				success = wallpaper_manager.start_image_animation(
					image_folder_path,
					frame_rate=15  # フレームレートは必要に応じて調整
				)
				if not success:
					return jsonify({"status": "error", "message": "アニメーションの開始に失敗しました"}), 500
		else:
			if wallpaper_manager.is_running:
				wallpaper_manager.stop_animation()

		# 設定を保存
		save_settings()
		logging.info("設定を更新しました: %s", animal_settings)

		# 正常に更新された場合のレスポンス
		return jsonify({"status": "success", "settings": animal_settings})

	except Exception as e:
		logging.error("エラーが発生しました: %s", str(e), exc_info=True)
		return jsonify({"status": "error", "message": str(e)}), 500


# サーバー起動時に設定を読み込む
if __name__ == '__main__':
	load_settings()
	app.run(port=5000)
