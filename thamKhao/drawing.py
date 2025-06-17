import pygame
import math

def draw_grid(surface, grid_size, draw_area):
    for x in range(draw_area.x, draw_area.x + draw_area.width,grid_size):
        pygame.draw.line(surface, (200, 200, 200), (x, draw_area.y), (x, draw_area.y + draw_area.height))
    for y in range(draw_area.y, draw_area.y + draw_area.height, grid_size):
        pygame.draw.line(surface, (200, 200, 200), (draw_area.x, y), (draw_area.x + draw_area.width, y))

def draw_axes_2d(surface, draw_area):
    center_x, center_y = draw_area.x + draw_area.width // 2, draw_area.y + draw_area.height // 2
    pygame.draw.line(surface, (0, 0, 0), (draw_area.x, center_y), (draw_area.x + draw_area.width, center_y))  # Trục X
    pygame.draw.line(surface, (0, 0, 0), (center_x, draw_area.y), (center_x, draw_area.y + draw_area.height))  # Trục Y

def midpoint_line(surface, x1, y1, x2, y2, color):
    # Thuật toán Midpoint để vẽ đoạn thẳng
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        y = y1
        d = 2 * dy - dx
        incrE = 2 * dy
        incrNE = 2 * (dy - dx)
        x = x1
        while x <= x2:
            surface.set_at((x, y), color)
            x += 1
            if d <= 0:
                d += incrE
            else:
                y += 1 if dy >= 0 else -1
                d += incrNE
    else:
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        x = x1
        d = 2 * dx - dy
        incrN = 2 * dx
        incrNE = 2 * (dx - dy)
        y = y1
        while y <= y2:
            surface.set_at((x, y), color)
            y += 1
            if d <= 0:
                d += incrN
            else:
                x += 1 if dx >= 0 else -1
                d += incrNE

def draw_circle(surface, x0, y0, radius, color):
    # Thuật toán Bresenham để vẽ hình tròn
    x = radius
    y = 0
    err = 0
    while x >= y:
        surface.set_at((x0 + x, y0 + y), color)
        surface.set_at((x0 + y, y0 + x), color)
        surface.set_at((x0 - y, y0 + x), color)
        surface.set_at((x0 - x, y0 + y), color)
        surface.set_at((x0 - x, y0 - y), color)
        surface.set_at((x0 - y, y0 - x), color)
        surface.set_at((x0 + y, y0 - x), color)
        surface.set_at((x0 + x, y0 - y), color)
        y += 1
        if err <= 0:
            err += 2 * y + 1
        else:
            x -= 1
            err += 2 * (y - x) + 1

def snap_to_grid(x, y, grid_size):
    return (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)

def project_cavalier(point_3d, draw_area):
    x, y, z = point_3d
    center_x, center_y = draw_area.x + draw_area.width // 2, draw_area.y + draw_area.height // 2
    # Phép chiếu cavalier: góc 45 độ, tỷ lệ chiều sâu 0.5
    xp = center_x + x + 0.5 * z
    yp = center_y - y + 0.5 * z
    return (xp, yp)

def draw_axes_3d(surface, draw_area):
    center_x, center_y = draw_area.x + draw_area.width // 2, draw_area.y + draw_area.height // 2
    # Vẽ trục X, Y, Z bằng phép chiếu cavalier
    x_axis = project_cavalier((100, 0, 0), draw_area)
    y_axis = project_cavalier((0, 100, 0), draw_area)
    z_axis = project_cavalier((0, 0, 100), draw_area)
    pygame.draw.line(surface, (255, 0, 0), (center_x, center_y), x_axis)  # Trục X
    pygame.draw.line(surface, (0, 255, 0), (center_x, center_y), y_axis)  # Trục Y
    pygame.draw.line(surface, (0, 0, 255), (center_x, center_y), z_axis)  # Trục Z

def draw_cube(surface, vertices, projection_type, draw_area):
    # Chiếu các đỉnh và vẽ các cạnh
    projected = [project_cavalier(v, draw_area) for v in vertices]
    edges = [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    for edge in edges:
        pygame.draw.line(surface, (0, 0, 0), projected[edge[0]], projected[edge[1]])