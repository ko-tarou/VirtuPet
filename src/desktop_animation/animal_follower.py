import tkinter as tk
import pyautogui
import time

# ウィンドウを作成
root = tk.Tk()
root.title("Moving Animal")
root.geometry("100x100")  # ウィンドウのサイズを画像のサイズに合わせる
root.attributes("-transparentcolor", "white")  # 背景を透明に

# 動物の画像を表示
canvas = tk.Canvas(root, width=100, height=100, bg='white', highlightthickness=0)
canvas.pack()
animal_img = tk.PhotoImage(file="path/to/your/animal.png")
canvas.create_image(0, 0, anchor=tk.NW, image=animal_img)

# 動物の追従関数
def follow_mouse():
    while True:
        x, y = pyautogui.position()  # マウスの現在位置を取得
        root.geometry(f"+{x}+{y}")  # ウィンドウの位置を更新
        time.sleep(0.01)  # 更新速度

# 別スレッドで追従を開始
import threading
follow_thread = threading.Thread(target=follow_mouse, daemon=True)
follow_thread.start()

# メインループ
root.mainloop()
