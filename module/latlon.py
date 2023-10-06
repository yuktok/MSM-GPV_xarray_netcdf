import numpy as np

#一番近い格子点を得るための関数
def get_closest_latlon(lat, lon):
    x = np.arange(22.4,47.6+0.05, 0.05)
    y = np.arange(120,150+0.0625,0.0625)
    X, Y = np.meshgrid(x, y)
    grid_points = np.column_stack((X.ravel(), Y.ravel()))
    # 点と格子点の距離を計算
    distances = np.sqrt(np.sum((grid_points -(lat, lon))**2, axis=1))
    # 距離が最小の格子点のインデックスを取得
    closest_grid_point_index = np.argmin(distances)
    #     距離が最小の格子点の座標を取得
    closest_grid_point = grid_points[closest_grid_point_index]
    print("最も近い格子点の座標:", closest_grid_point)
    #roundを用いて丸めないと微小な誤差が入ってることがある（原因不明）
    return np.round(closest_grid_point,3)