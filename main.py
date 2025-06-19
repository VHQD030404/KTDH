import pygame
from pygame import Vector2
import math
import numpy as np

"""---------------------------------PHẦN SETTING---------------------------------"""
W, H = 1280, 720
UNIT_SIZE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN_NAVY = (107, 142, 35)
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
draw_area = pygame.Rect(0, -50, 800, 800)  # rect khu vực vẽ hình
current_mode = '2D mode'
font = pygame.font.SysFont('arial', 20)
"""---------------------------------PHẦN UI---------------------------------"""

buttons = [
    {"rect": pygame.Rect(820, 50, 110, 40), "text": "2D mode"},
    {"rect": pygame.Rect(820, 100, 110, 40), "text": "Đồng hồ"},
    {"rect": pygame.Rect(820, 150, 110, 40), "text": "tank"},
    {"rect": pygame.Rect(950, 50, 110, 40), "text": "duong thang"},
    {"rect": pygame.Rect(950, 100, 110, 40), "text": "hinh chu nhat"},
    {"rect": pygame.Rect(950, 150, 110, 40), "text": "hinh tron"},
    {"rect": pygame.Rect(1070, 50, 110, 40), "text": "hinh thang"},
    {"rect": pygame.Rect(1070, 100, 110, 40), "text": "hinh vuong"},
    {"rect": pygame.Rect(820, 200, 100, 40), "text": "3D mode"},
    {"rect": pygame.Rect(950, 200, 100, 40), "text": "Ve hinh___"},
    {"rect": pygame.Rect(950, 250, 100, 40), "text": "Ve hinh___"},
    {"rect": pygame.Rect(820, 300, 120, 40), "text": "XOÁ DU LIEU"},
    {"rect": pygame.Rect(1000, 550, 100, 40), "text": "XÓA"},
    {"rect": pygame.Rect(1000, 500, 100, 40), "text": "NHAP"},
    {"rect": pygame.Rect(820, 400, 120, 40), "text": "TINH TIEN"},
]
input_boxes = [
    {"rect": pygame.Rect(880, 450, 100, 30), "label": "dx:", "value": "", "active": False},
    {"rect": pygame.Rect(880, 500, 100, 30), "label": "dy:", "value": "", "active": False},
    {"rect": pygame.Rect(880, 550, 100, 30), "label": "X:", "value": "", "active": False},
    {"rect": pygame.Rect(880, 600, 100, 30), "label": "Y:", "value": "", "active": False},
    {"rect": pygame.Rect(880, 650, 100, 30), "label": "Z:", "value": "", "active": False},

]
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

"""---------------------------------CÁC HÀM BIẾN ĐỔI---------------------------------"""

"""---------------------------------PHẦN HÀM VẼ HÌNH 2D---------------------------------"""
# Thêm biến để lưu hình cần vẽ
current_shape = None
shape_points = []  # Lưu các điểm của hình đang vẽ
inputpoint_data = []
points = []
drawn_shapes = []

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


def draw_rectangle(start, end, color=BLACK, fill_color= None):
    """Vẽ hình chữ nhật từ start (góc trên trái) đến end (góc dưới phải)"""
    x1, y1 = start
    x2, y2 = end
    if fill_color:
        step = 0.1  # Bước nhảy (có thể điều chỉnh)
        for y in np.arange(y1, y2 + step, step):
            draw_line((x1, y), (x2, y), fill_color)
    # Vẽ 4 cạnh của hình chữ nhật
    draw_line((x1, y1), (x2, y1), color)  # Cạnh trên
    draw_line((x2, y1), (x2, y2), color)  # Cạnh phải
    draw_line((x2, y2), (x1, y2), color)  # Cạnh dưới
    draw_line((x1, y2), (x1, y1), color)  # Cạnh trái


def draw_circle(center, radius, color=BLACK, fill_color=None):
    """Vẽ hình tròn sử dụng thuật toán Midpoint với tùy chọn tô màu nền"""
    x0, y0 = center
    x = radius
    y = 0
    err = 0

    border_points = set()

    # Vẽ đường viền và lưu các điểm biên
    while x >= y:
        # 8 điểm đối xứng
        points = [
            (x0 + x, y0 + y), (x0 + y, y0 + x),
            (x0 - y, y0 + x), (x0 - x, y0 + y),
            (x0 - x, y0 - y), (x0 - y, y0 - x),
            (x0 + y, y0 - x), (x0 + x, y0 - y)
        ]

        for point in points:
            putPixel(point, color)
            border_points.add((point[0], point[1]))

        y += 1
        err += 1 + 2 * y
        if 2 * (err - x) + 1 > 0:
            x -= 1
            err += 1 - 2 * x

    # Nếu có màu nền, thực hiện tô màu bằng thuật toán scanline(dùng để vẽ tank)
    if fill_color is not None:
        # Chuyển border_points thành dictionary để dễ truy cập theo y
        scan_lines = {}
        for (px, py) in border_points:
            if py not in scan_lines:
                scan_lines[py] = []
            scan_lines[py].append(px)

        # Sắp xếp các giá trị y để quét từ trên xuống hoặc từ dưới lên
        sorted_ys = sorted(scan_lines.keys())

        for y in sorted_ys:
            x_values = scan_lines[y]
            if len(x_values) < 2:
                continue  # Bỏ qua nếu không đủ điểm để tạo đoạn

            x_min = min(x_values)
            x_max = max(x_values)
            step = 0.1
            # Tô màu các điểm giữa x_min và x_max
            for x in np.arange(x_min + 1, x_max, step):
                if (x, y) not in border_points:  # Chỉ tô nếu không phải điểm biên
                    putPixel((x, y), fill_color)

            # Cập nhật giao diện sau mỗi dòng quét để tránh Not Responding
            if y % 5 == 0:  # Cập nhật sau mỗi 5 dòng để cân bằng hiệu năng
                if hasattr(putPixel, '__gui_update__'):
                    putPixel.__gui_update__()
                else:
                    try:
                        import time
                        time.sleep(0.001)  # Nhường CPU nếu cần
                    except:
                        pass


def draw_trapezoid(points, color=BLACK, fill_color=GREEN):
    """Vẽ hình thang cân từ 2 điểm (đáy lớn) và tự tính đáy nhỏ"""
    if len(points) < 2:
        return

    p1, p2 = points[0], points[1]

    # Kiểm tra 2 điểm trùng nhau
    if math.dist(p1, p2) < 1e-6:
        return

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    base_length = math.hypot(dx, dy)

    # Tính toán các điểm
    small_base = base_length * 0.6
    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2

    # Vector vuông góc chuẩn hóa
    perp_dx = -dy / base_length
    perp_dy = dx / base_length

    if perp_dy > 0:
        perp_dx = -perp_dx
        perp_dy = -perp_dy
    height = base_length * 0.4
    top_mid_x = mid_x + perp_dx * height
    top_mid_y = mid_y + perp_dy * height

    # Tính 2 điểm đáy nhỏ
    p3 = (top_mid_x - small_base / 2 * dx / base_length,
          top_mid_y - small_base / 2 * dy / base_length)
    p4 = (top_mid_x + small_base / 2 * dx / base_length,
          top_mid_y + small_base / 2 * dy / base_length)
    if fill_color is not None:
        # Tìm bounding box
        min_y = min(p1[1], p2[1], p3[1], p4[1])
        max_y = max(p1[1], p2[1], p3[1], p4[1])

        # Quét từng dòng để tô màu
        for y in range(int(min_y), int(max_y) + 1):
            # Tìm giao điểm với các cạnh
            intersections = []
            edges = [(p1, p3), (p3, p4), (p4, p2), (p2, p1)]

            for edge_start, edge_end in edges:
                x_intersect = find_intersection_y(edge_start, edge_end, y)
                if x_intersect is not None:
                    intersections.append(x_intersect)

            if len(intersections) >= 2:
                # Vẽ đường ngang giữa các giao điểm
                draw_line((min(intersections), y), (max(intersections), y), fill_color)
    # Vẽ hình thang
    draw_line(p1, p2, color)
    draw_line(p2, p4, color)
    draw_line(p4, p3, color)
    draw_line(p3, p1, color)


def find_intersection_y(p1, p2, y):
    """Tìm giao điểm của đường thẳng p1-p2 với đường ngang y"""
    x1, y1 = p1
    x2, y2 = p2

    # Kiểm tra nếu đoạn thẳng nằm ngang
    if y1 == y2:
        return None if y != y1 else min(x1, x2)

    # Kiểm tra nếu y nằm ngoài khoảng y của đoạn thẳng
    if (y < min(y1, y2)) or (y > max(y1, y2)):
        return None

    # Tính x theo phương trình đường thẳng
    t = (y - y1) / (y2 - y1)
    x = x1 + t * (x2 - x1)
    return x

def draw_square(points, color=BLACK):
    """Vẽ hình vuông từ 2 điểm (điểm 1 là góc, điểm 2 xác định cạnh)"""
    if len(points) < 2:
        return

    x1, y1 = points[0]
    x2, y2 = points[1]

    # Tính độ dài cạnh (lấy theo cạnh ngắn hơn)
    dx = x2 - x1
    dy = y2 - y1
    side_length = min(abs(dx), abs(dy))

    # Xác định hướng
    if dx < 0:
        side_length = -side_length
    if dy < 0:
        side_length = -side_length

    # Tính các điểm còn lại
    x3 = x1 + side_length
    y3 = y1
    x4 = x1 + side_length
    y4 = y1 + side_length
    x5 = x1
    y5 = y1 + side_length

    # Vẽ 4 cạnh hình vuông
    draw_line((x1, y1), (x3, y3), color)
    draw_line((x3, y3), (x4, y4), color)
    draw_line((x4, y4), (x5, y5), color)
    draw_line((x5, y5), (x1, y1), color)


def draw_clock(center_point, color=BLACK):
    """Vẽ đồng hồ analog với đồng hồ phụ hiển thị giây"""
    main_x, main_y = center_point
    main_radius = 150  # Bán kính đồng hồ chính

    # Vẽ đồng hồ chính (giờ và phút)
    draw_circle(center_point, main_radius)
    putPixel(center_point, RED)  # Tâm đồng hồ

    # Vẽ các vạch chỉ giờ
    for hour in range(1, 13):
        angle = math.radians(hour * 30 - 90)
        start_x = main_x + (main_radius - 15) * math.cos(angle)
        start_y = main_y + (main_radius - 15) * math.sin(angle)
        end_x = main_x + main_radius * math.cos(angle)
        end_y = main_y + main_radius * math.sin(angle)
        draw_line((start_x, start_y), (end_x, end_y), color)

    # Lấy thời gian hiện tại
    import datetime
    now = datetime.datetime.now()
    hours, minutes, seconds = now.hour % 12, now.minute, now.second

    # Vẽ kim giờ
    hour_angle = math.radians(hours * 30 + minutes * 0.5 - 90)
    hour_end = (main_x + main_radius * 0.5 * math.cos(hour_angle),
                main_y + main_radius * 0.5 * math.sin(hour_angle))
    draw_line(center_point, hour_end, BLACK)

    # Vẽ kim phút
    minute_angle = math.radians(minutes * 6 - 90)
    minute_end = (main_x + main_radius * 0.7 * math.cos(minute_angle),
                  main_y + main_radius * 0.7 * math.sin(minute_angle))
    draw_line(center_point, minute_end, BLUE)

    # Vẽ đồng hồ phụ (giây) - đặt phía dưới đồng hồ chính
    sec_center = (main_x, main_y + main_radius - 60)  # Cách đồng hồ chính 30px
    sec_radius = main_radius// 5  # Bán kính đồng hồ phụ

    # Vẽ vòng tròn đồng hồ phụ
    draw_circle(sec_center, sec_radius)
    putPixel(sec_center, BLUE)  # Tâm đồng hồ phụ
    # Vẽ vạch chỉ giây (mỗi 5 giây một vạch lớn)
    for second in range(0, 60, 5):
        angle = math.radians(second * 6 - 90)  # 6 độ mỗi giây
        # Vạch dài hơn cho các mốc 15, 30, 45, 60 giây
        is_major = second % 15 == 0
        inner_offset = 15 if is_major else 15  # Giảm khoảng cách từ biên
        outer_offset = 0 if is_major else 5  # Giảm khoảng cách từ biên

        # Tính toán vị trí bắt đầu và kết thúc của vạch
        start_x = sec_center[0] + (sec_radius - inner_offset +5) * math.cos(angle)
        start_y = sec_center[1] + (sec_radius - inner_offset+5) * math.sin(angle)
        end_x = sec_center[0] + (sec_radius - outer_offset) * math.cos(angle)
        end_y = sec_center[1] + (sec_radius - outer_offset) * math.sin(angle)
        draw_line((start_x, start_y), (end_x, end_y), color)
    # Vẽ kim giây (trên đồng hồ phụ)
    second_angle = math.radians(seconds * 6 - 90)
    second_end = (sec_center[0] + sec_radius * 0.5 * math.cos(second_angle),
                  sec_center[1] + sec_radius * 0.5 * math.sin(second_angle))
    draw_line(sec_center, second_end, RED)


def draw_tank(center_point, radius=20, color=BLACK, fill_color=GREEN_NAVY):
    """Vẽ 4 hình tròn cùng bán kính theo hàng ngang"""
    rect_height = radius
    # Lấy tọa độ x, y từ tuple center_point
    x, y = center_point[0], center_point[1]  # Giải nén tuple
    spacing = radius * 3  # Khoảng cách giữa các hình tròn
    #bánh xe
    draw_rectangle(start= (x - spacing * 1.5, y - radius), end=(x + spacing * 1.5, y + radius), color=color, fill_color=fill_color )
    for i in range(4):
        circle_x = x + (i - 1.5) * spacing  # Tính toán vị trí để căn giữa
        draw_circle((circle_x, y), radius, color, fill_color=BLACK)


    trapezoid_height = radius * 3
    top_y = y - radius - trapezoid_height
    #nòng pháo
    rect_top = top_y - rect_height
    draw_rectangle(
        start=(x + spacing + 100, top_y + 10),
        end=(x - spacing + 50, rect_top + 70),
        color=color,
        fill_color=fill_color  # Thêm màu nền
    )
    #thân xe
    trapezoid_top_y = y + radius + trapezoid_height
    bottom_left = (x - spacing * 1.5, y - radius)  # Điểm trái đáy lớn
    bottom_right = (x + spacing * 1.5, y - radius)  # Điểm phải đáy lớn

    draw_trapezoid(
        points=[bottom_left, bottom_right, trapezoid_top_y],  # 2 điểm đáy lớn
        color=color,
        fill_color=fill_color  # Sử dụng màu nền được truyền vào
    )

def draw_shape(shape_type, points):
    """Vẽ hình dựa trên loại hình và các điểm"""
    if len(points) < 2:
        return

    if shape_type == "duong thang":
        draw_line(points[0], points[1])
    elif shape_type == "hinh chu nhat":
        draw_rectangle(points[0], points[1])
    elif shape_type == "hinh tron":
        # Tính bán kính từ khoảng cách giữa 2 điểm
        x1, y1 = points[0]
        x2, y2 = points[1]
        radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        draw_circle(points[0], radius)
    elif shape_type == "hinh thang":
        draw_trapezoid(points)
    elif shape_type == "hinh vuong":
        draw_square(points)
    elif shape_type == "Đồng hồ":
        if len(points) == 2:
            # Tính bán kính từ khoảng cách 2 điểm
            radius = int(math.dist(points[0], points[1]))
            draw_clock(points[0], radius)
    if shape_type == "tank":
        if len(points) >= 1:
            draw_tank(points[0])

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
        print(f"Debug - Điểm {len(shape_points)}")
        if len(shape_points) == 2:
            # Lưu hình đã vẽ vào danh sách
            drawn_shapes.append({
                'type': current_shape,
                'points': shape_points.copy(),
                'time': pygame.time.get_ticks() // 1000  # Lưu thời gian tạo
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
            if shape['type'] == "Đồng hồ":
                # Tính thời gian đã trôi qua kể từ khi tạo đồng hồ
                time_passed = (pygame.time.get_ticks() // 1000) - shape['time']
                draw_clock(shape['points'][0],
                           int(math.dist(shape['points'][0], shape['points'][1])),
                           time_passed)
            else:
                draw_shape(shape['type'], shape['points'])

            # Vẽ hình tạm thời khi đang kéo chuột
        if current_shape and len(shape_points) == 1:
            mouse_pos = pygame.mouse.get_pos()
            if draw_area.collidepoint(mouse_pos):
                if current_shape == "tank":
                    # Chỉ cần 1 điểm cho 4 hình tròn
                    temp_points = [revert_pos(convert_pos(mouse_pos))]
                    draw_tank(temp_points[0])
                else:
                    # Xử lý các hình khác như cũ
                    temp_points = shape_points.copy()
                    temp_points.append(revert_pos(convert_pos(mouse_pos)))
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
                    elif button["text"] in ["duong thang", "hinh chu nhat", "hinh tron", "hinh thang", "hinh vuong", "Đồng hồ", "tank"]:
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