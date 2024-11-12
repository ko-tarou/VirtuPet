from flask import Flask, request, jsonify
from wallpaper_manager import WallpaperManager

app = Flask(__name__)
wallpaper_manager = WallpaperManager()

animal_settings = {
    "size": 1.0,
    "is_visible": True
}

@app.route('/get_animal_settings', methods=['GET'])
def get_animal_settings():
    return jsonify(animal_settings)

@app.route('/set_animal_settings', methods=['POST'])
def set_animal_settings():
    data = request.json
    if "size" in data:
        animal_settings["size"] = data["size"]
    if "is_visible" in data:
        animal_settings["is_visible"] = data["is_visible"]

    if animal_settings["is_visible"]:
        wallpaper_manager.start_animation(animal_settings["size"])
    else:
        wallpaper_manager.stop_animation()

    return jsonify({"status": "success", "settings": animal_settings})

if __name__ == '__main__':
    app.run(port=5000)
