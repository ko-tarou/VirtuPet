from flask import Flask, request, jsonify
from flask_cors import CORS  # 追加
from wallpaper_manager import WallpaperManager

app = Flask(__name__)
CORS(app)  # CORSを有効にする
manager = WallpaperManager()

@app.route('/change_wallpaper', methods=['POST'])
def change_wallpaper():
    print("API called")  # APIが呼ばれたときのログ
    data = request.get_json()
    image_path = data.get('image_path')
    if image_path:
        manager.switch_wallpaper(image_path)
        return jsonify({"status": "success", "message": "Wallpaper changed"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid image path"}), 400

if __name__ == "__main__":
    app.run(port=5000)
