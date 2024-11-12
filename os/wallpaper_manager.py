import pygame
import threading
import subprocess
import sys
import os

class WallpaperManager:
    def __init__(self):
        pygame.init()
        self.is_animating = False
        self.animation_thread = None
        self.animal_follower_process = None
        self.lock = threading.Lock()

    def start_animation(self, size):
        with self.lock:
            if not self.is_animating:
                self.is_animating = True
                script_path = os.path.abspath("../desktop_animation/animal_follower.py")
                # size引数をコマンドライン引数として渡す
                self.animal_follower_process = subprocess.Popen([sys.executable, script_path, str(size)])
                print("animal_follower.py started with size:", size)

    def stop_animation(self):
        with self.lock:
            self.is_animating = False
            if self.animal_follower_process is not None:
                self.animal_follower_process.terminate()
                self.animal_follower_process = None
                print("animal_follower.py stopped.")
