def object_pos(toponym_coodrinates_1, toponym_coodrinates_2):
    x_1, y_1 = toponym_coodrinates_1.split(" ")
    x_2, y_2 = toponym_coodrinates_2.split(" ")
    x_1, y_1 = float(x_1), float(y_1)
    x_2, y_2 = float(x_2), float(y_2)
    if x_2 < x_1:
        x_2, x_1 = x_1, x_2
    if y_2 < y_1:
        y_2, y_1 = y_1, y_2
    toponym_longitude, toponym_lattitude = str(((x_2 - x_1) / 2) + x_1), str(((y_2 - y_1) / 2) + y_1)

    delta_x = str(float(toponym_longitude) - x_1 * 0.999777)
    delta_y = str(float(toponym_lattitude) - y_1 * 0.999777)
    return toponym_longitude, toponym_lattitude, delta_x, delta_y
