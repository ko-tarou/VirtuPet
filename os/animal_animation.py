class AnimalAnimation:
    def __init__(self, speed=5):
        self.x = 100  # 初期位置X
        self.y = 100  # 初期位置Y
        self.speed = speed  # 移動速度

    def smooth_move(self, target_x, target_y):
        """動物の位置を滑らかに移動する"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < self.speed:
            return target_x, target_y
        self.x += self.speed * dx / distance
        self.y += self.speed * dy / distance
        return self.x, self.y

    def update_position(self, target_x, target_y):
        """位置更新ロジックをここで変更可能"""
        # 必要に応じて、複雑なアニメーションロジックをここに記述
        return self.smooth_move(target_x, target_y)
