import pygame
from pygame import Vector2
import math

"""---------------------------------PHẦN SETTING---------------------------------"""
W, H = 1280, 720
UNIT_SIZE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
draw_area = pygame.Rect(0, -50, 800, 800)  # rect khu vực vẽ hình
current_mode = '2D mode'
font = pygame.font.SysFont('arial', 20)
"""---------------------------------PHẦN UI---------------------------------"""

buttons = [
    {"rect": pygame.Rect(820, 50, 100, 40), "text": "2D mode"},
    {"rect": pygame.Rect(950, 50, 100, 40), "text": "Line"},
    {"rect": pygame.Rect(950, 100, 100, 40), "text": "Rectangle"},
    {"rect": pygame.Rect(950, 150, 100, 40), "text": "Circle"},
    {"rect": pygame.Rect(820, 200, 100, 40), "text": "3D mode"},
    {"rect": pygame.Rect(950, 200, 100, 40), "text": "Ve hinh___"},
    {"rect": pygame.Rect(950, 250, 100, 40), "text": "Ve hinh___"},
    {"rect": pygame.Rect(820, 300, 120, 40), "text": "XOÁ DU LIEU"},
    {"rect": pygame.Rect(1000, 550, 100, 40), "text": "XÓA"},
    {"rect": pygame.Rect(1000, 500, 100, 40), "text": "NHAP"},
]
input_boxes = [
    {"rect": pygame.Rect(880, 500, 100, 30), "label": "X:", "value": "", "active": False},
    {"rect": pygame.Rect(880, 540, 100, 30), "label": "Y:", "value": "", "active": False},
    {"rect": pygame.Rect(880, 580, 100, 30), "label": "Z:", "value": "", "active": False}
]

# Thêm biến để lưu hình cần vẽ
current_shape = None
shape_points = []  # Lưu các điểm của hình đang vẽ
inputpoint_data = []
points = []
drawn_shapes = []

def draw_UI(screen, font):
    for button in buttons:
        color = (150, 150, 150) if current_mode != button["text"] else (100, 100, 255)
        pygame.draw.rect(screen, color, button["rect"])
        text = font.render(button["text"], True, (255, 255, 255))
        text_rect = text.get_rect(center=button["rect"].center)
        screen.blit(text, text_rect)
    for box in input_boxes:
        if current_mode == '2D mode' and box["label"] == "Z:":  # Bỏ ô Z ở 2D mode
            continue
        color = (0, 255, 0) if box["active"] else (0, 0, 0)
        pygame.draw.rect(screen, color, box["rect"], 2)
        # Hiển thị text trong ô
        text_surface = font.render(f"{box['value']}", True, (0, 0, 0))
        screen.blit(text_surface, (box["rect"].x + 30, box["rect"].y + 5))  # Dịch text sang phải sau nhãn
        # Vẽ nhãn bên trái ô
        label_surface = font.render(box["label"], True, (0, 0, 0))
        screen.blit(label_surface, (box["rect"].x - 25, box["rect"].y + 5))


"""---------------------------------PHẦN HÀM VẼ HÌNH 2D---------------------------------"""


def draw_line(start, end, color=BLACK):
    """Vẽ đường thẳng từ start đến end sử dụng thuật toán Bresenham"""
    x1, y1 = start
    x2, y2 = end

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    error = dx // 2
    ystep = 1 if y1 < y2 else -1

    y = y1
    for x in range(int(x1), int(x2) + 1):
        coord = (y, x) if steep else (x, y)
        putPixel(coord, color)
        error -= dy
        if error < 0:
            y += ystep
            error += dx


def draw_rectangle(start, end, color=BLACK):
    """Vẽ hình chữ nhật từ start (góc trên trái) đến end (góc dưới phải)"""
    x1, y1 = start
    x2, y2 = end

    # Vẽ 4 cạnh của hình chữ nhật
    draw_line((x1, y1), (x2, y1), color)  # Cạnh trên
    draw_line((x2, y1), (x2, y2), color)  # Cạnh phải
    draw_line((x2, y2), (x1, y2), color)  # Cạnh dưới
    draw_line((x1, y2), (x1, y1), color)  # Cạnh trái


def draw_circle(center, radius, color=BLACK):
    """Vẽ hình tròn sử dụng thuật toán Midpoint"""
    x0, y0 = center
    x = radius
    y = 0
    err = 0

    while x >= y:
        putPixel((x0 + x, y0 + y), color)
        putPixel((x0 + y, y0 + x), color)
        putPixel((x0 - y, y0 + x), color)
        putPixel((x0 - x, y0 + y), color)
        putPixel((x0 - x, y0 - y), color)
        putPixel((x0 - y, y0 - x), color)
        putPixel((x0 + y, y0 - x), color)
        putPixel((x0 + x, y0 - y), color)

        y += 1
        err += 1 + 2 * y
        if 2 * (err - x) + 1 > 0:
            x -= 1
            err += 1 - 2 * x


def draw_shape(shape_type, points):
    """Vẽ hình dựa trên loại hình và các điểm"""
    if len(points) < 2:
        return

    if shape_type == "Line":
        draw_line(points[0], points[1])
    elif shape_type == "Rectangle":
        draw_rectangle(points[0], points[1])
    elif shape_type == "Circle":
        # Tính bán kính từ khoảng cách giữa 2 điểm
        x1, y1 = points[0]
        x2, y2 = points[1]
        radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        draw_circle(points[0], radius)


"""---------------------------------PHẦN HÀM CHUNG---------------------------------"""


def set_mode(mode):
    """Chuyển đổi giữa 2D mode và 3D mode"""
    global current_mode, current_shape, shape_points
    if mode in ['2D mode', '3D mode']:
        current_mode = mode
        current_shape = None
        shape_points = []
    else:
        print("Mode không hợp lệ! Chọn '2D' hoặc '3D'")
        return
    print(f"Chuyển sang {mode}")


def putPixel(pos, color=BLACK):
    """nhập vào pos kiểu list hoặc tuple 2 phần tử (x,y)"""
    pygame.draw.rect(screen, color,
                     (pos[0] - UNIT_SIZE // 2,
                      pos[1] - UNIT_SIZE // 2,
                      UNIT_SIZE, UNIT_SIZE))


def draw_grid(screen, grid_size, draw_area):
    for x in range(draw_area.x, draw_area.x + draw_area.width, grid_size):  # grid size là step
        pygame.draw.line(screen, GRAY, (x, draw_area.y), (x, draw_area.y + draw_area.height))  # VẼ GRID Y
    for y in range(draw_area.y, draw_area.y + draw_area.height, grid_size):
        pygame.draw.line(screen, GRAY, (draw_area.x, y), (draw_area.x + draw_area.width, y))  # VẼ GRID X


def draw_axes_2d(screen, draw_area=draw_area):
    center_x, center_y = draw_area.x + draw_area.width // 2, draw_area.y + draw_area.height // 2
    pygame.draw.line(screen, BLACK, (draw_area.x, center_y), (draw_area.x + draw_area.width, center_y))  # Trục X
    pygame.draw.line(screen, BLACK, (center_x, draw_area.y), (center_x, draw_area.y + draw_area.height))  # Trục Y


def project_cabinet(x, y, z):
    """Nhập vào tọa độ 3d theo hệ tự vẽ, trả về tọa độ 2d theo hệ pygame"""
    center_x = draw_area.x + draw_area.width / 2
    center_y = draw_area.y + draw_area.height / 2
    angle = math.radians(225)
    scale_z = 0.5
    # Tính tọa độ 2D trong hệ tự vẽ
    proj_x = x + scale_z * z * math.cos(angle)
    proj_y = y + scale_z * z * math.sin(angle)
    # Chuyển sang hệ Pygame
    pygame_x = center_x + proj_x * UNIT_SIZE
    pygame_y = center_y - proj_y * UNIT_SIZE  # Đảo y
    return (pygame_x, pygame_y)


def draw_3d_axes(screen, axis_length=100):
    """Vẽ hệ tọa độ 3D dùng phép chiếu cabinet"""
    # tọa độ theo hệ tự vẽ:
    x_axis_end = (axis_length, 0, 0)  # Trục x
    y_axis_end = (0, axis_length, 0)  # Trục y
    z_axis_end = (0, 0, axis_length)  # Trục z

    # Chuyển đổi các điểm đầu cuối trục sang tọa độ Pygame
    origin = project_cabinet(0, 0, 0)  # điểm O
    x_end = project_cabinet(*x_axis_end)  # dùng * để lấy giá trị 3 tọa độ thay vì lấy cả tuple
    y_end = project_cabinet(*y_axis_end)
    z_end = project_cabinet(*z_axis_end)

    # Vẽ các trục
    pygame.draw.line(screen, RED, origin, x_end, 2)
    pygame.draw.line(screen, GREEN, origin, y_end, 2)
    pygame.draw.line(screen, BLUE, origin, z_end, 2)

    # Ghi nhãn trục
    font = pygame.font.SysFont('arial', 15)
    screen.blit(font.render('X', True, (255, 0, 0)), (x_end[0] + 5, x_end[1]))
    screen.blit(font.render('Y', True, (0, 255, 0)), (y_end[0], y_end[1] - 20))
    screen.blit(font.render('Z', True, (0, 0, 255)), (z_end[0] + 5, z_end[1]))


def convert_pos(pos):
    """Chuyển đổi từ hệ tọa độ pygame sang hệ tọa độ tự vẽ"""
    center_x = draw_area.x + draw_area.width / 2
    center_y = draw_area.y + draw_area.height / 2
    x, y = pos
    rel_x = round((x - center_x) / UNIT_SIZE)  # Làm tròn 5px
    rel_y = round((center_y - y) / UNIT_SIZE)  # Đảo y và làm tròn
    rel_pos = (rel_x, rel_y)
    return rel_pos


def revert_pos(rel_pos):
    """Chuyển đổi từ tọa độ tự vẽ về tọa độ pygame"""
    center_x = draw_area.x + draw_area.width / 2
    center_y = draw_area.y + draw_area.height / 2
    rel_x, rel_y = rel_pos
    x = rel_x * UNIT_SIZE + center_x
    y = center_y - rel_y * UNIT_SIZE
    return (x, y)


def click_mouse_pos(pos):
    global shape_points, drawn_shapes

    pos = revert_pos(convert_pos(pos))

    if current_shape:
        shape_points.append(pos)

        if len(shape_points) == 2:
            # Lưu hình đã vẽ vào danh sách
            drawn_shapes.append({
                'type': current_shape,
                'points': [shape_points[0], shape_points[1]]
            })
            shape_points = []


def update_scene():
    global current_mode, current_shape, shape_points
    if current_mode == '2D mode':
        draw_grid(screen, UNIT_SIZE, draw_area)
        draw_axes_2d(screen, draw_area)
        for dpoint in inputpoint_data:
            putPixel(dpoint[0])
            putPixel(dpoint[1])
        for shape in drawn_shapes:
            draw_shape(shape['type'], shape['points'])
        # Vẽ hình tạm thời khi đang chọn điểm
        if current_shape and len(shape_points) == 1:
            mouse_pos = pygame.mouse.get_pos()
            if draw_area.collidepoint(mouse_pos):
                temp_points = [shape_points[0], mouse_pos]
                draw_shape(current_shape, temp_points)
    elif current_mode == '3D mode':
        draw_3d_axes(screen)


running = True
while running:
    screen.fill(WHITE)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if draw_area.collidepoint(event.pos):
                click_mouse_pos(event.pos)

            # Kiểm tra xem có nhấn vào nút nào không
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    if button["text"] in ['2D mode', '3D mode']:
                        set_mode(button["text"])
                    elif button["text"] in ["Line", "Rectangle", "Circle"]:
                        current_shape = button["text"]
                        shape_points = []
                        print(f"Chọn vẽ hình: {current_shape}")
                    elif button["text"] == "XOÁ DU LIEU":
                        drawn_shapes = []
                        inputpoint_data = []
                        shape_points = []
                        inputpoint_data.clear()
                        for box in input_boxes:
                            box["value"] = ""
                    elif button["text"] == "XÓA":
                        for box in input_boxes:
                            box["value"] = ""
                    elif button["text"] == "NHAP":
                        if all(box["value"] for box in input_boxes[0:2]):
                            try:
                                x = int(input_boxes[0]["value"])
                                y = int(input_boxes[1]["value"])
                                z = int(input_boxes[2]["value"]) if current_mode == '3D mode' else 0
                                points.append((x, y, z) if current_mode == '3D mode' else revert_pos((x, y)))
                                click_count += 1
                                if click_count == 2:
                                    inputpoint_data.append(tuple(points))
                                    points.clear()
                                    click_count = 0
                                print(points)
                            except ValueError:
                                print("Lỗi nhập liệu, vui lòng nhập lại")

            for box in input_boxes:
                box["active"] = False
                if box["rect"].collidepoint(event.pos):
                    box["active"] = True

        elif event.type == pygame.KEYDOWN:
            for box in input_boxes:
                # NHẬN TEXT VÀO BOX
                if box["active"]:
                    if event.key == pygame.K_BACKSPACE:
                        box["value"] = box["value"][:-1]
                    elif event.key == pygame.K_RETURN:
                        box["active"] = False
                    elif event.unicode.isprintable() and len(box["value"]) < 10:
                        box["value"] += event.unicode

        elif event.type == pygame.QUIT:
            print(inputpoint_data)
            running = False

    update_scene()
    draw_UI(screen, font)
    pygame.display.update()

pygame.quit()