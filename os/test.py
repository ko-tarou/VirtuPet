import ctypes
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

class WallpaperManager:
    def __init__(self):
        self.original_wallpaper = self.get_current_wallpaper()
        self.new_wallpaper = None

    def get_current_wallpaper(self):
        """現在の壁紙のパスを取得する"""
        buffer = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(0x0073, len(buffer), buffer, 0)
        return buffer.value

    def set_wallpaper(self, image_path):
        """指定した画像を壁紙に設定する"""
        abs_image_path = os.path.abspath(image_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_image_path, 3)

    def switch_wallpaper(self, new_wallpaper_path):
        """現在の壁紙と新しい壁紙を入れ替える"""
        if self.new_wallpaper is None:
            # 新しい壁紙が未設定の場合、指定した壁紙を設定し、元の壁紙を保存
            self.new_wallpaper = new_wallpaper_path
            self.set_wallpaper(self.new_wallpaper)
        else:
            # 元の壁紙に戻す
            self.set_wallpaper(self.original_wallpaper)
            self.new_wallpaper = None

# インスタンスを生成
manager = WallpaperManager()

# APIエンドポイントの設定
@app.route("/api/set-wallpaper", methods=["POST"])
def set_wallpaper():
    data = request.get_json()
    image_path = data.get("image_path")

    if image_path:
        manager.switch_wallpaper(image_path)
        return jsonify({"status": "壁紙が変更されました"}), 200
    else:
        return jsonify({"error": "画像パスが無効です"}), 400

if __name__ == "__main__":
    app.run(port=5001)
