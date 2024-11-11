def smooth_move(current_x, current_y, target_x, target_y, speed=0.1):
    # 現在の位置と目標位置の間をスムーズに移動する
    new_x = current_x + (target_x - current_x) * speed
    new_y = current_y + (target_y - current_y) * speed
    return new_x, new_y
