import pygame
import math

# Cấu hình
WIDTH, HEIGHT = 800, 800
UNIT_SIZE = 3 #số pixel đại diện 1 đơn vị
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (200, 200, 200)

# Khởi tạo
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hệ tọa độ với nhập liệu")
font = pygame.font.SysFont('Arial', 12)

# Các nút chọn kiểu vẽ
mode_buttons = {
    "Doan Thang": pygame.Rect(20, HEIGHT-120, 90, 30),
    "Net Dut": pygame.Rect(120, HEIGHT-120, 90, 30),
    "Net Cham Gach": pygame.Rect(220, HEIGHT-120, 90, 30),
    "Mui Ten": pygame.Rect(320, HEIGHT-120, 90, 30),
    "Hinh Chu Nhat": pygame.Rect(420, HEIGHT-120, 90, 30)
}
selected_mode = "Doan Thang"  # Kiểu vẽ mặc định

# 2 ô nhập liệu và nút OK, Reset
input_boxes = [
    pygame.Rect(20, HEIGHT-80, 100, 30),  
    pygame.Rect(150, HEIGHT-80, 100, 30)  
]
ok_button = pygame.Rect(280, HEIGHT-80, 60, 30)
reset_button = pygame.Rect(360, HEIGHT-80, 80, 30)
input_texts = ["", ""]
input_active = [False, False]
points = [None, None]
labels = ["A (x0,y0)", "B (x1,y1)"]  # Nhãn mặc định

def putPixel(pixel_x, pixel_y, x, y, color=RED):
    pygame.draw.rect(screen, color, 
                   (pixel_x - UNIT_SIZE//2,
                    pixel_y - UNIT_SIZE//2,
                    UNIT_SIZE, UNIT_SIZE))

def draw_grid_and_axes():
    screen.fill(WHITE)
    
    pygame.draw.line(screen, BLACK, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2)
    pygame.draw.line(screen, BLACK, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
    
    for unit in range(-WIDTH//2//UNIT_SIZE, WIDTH//2//UNIT_SIZE + 1):
        if unit != 0:
            x_pos = WIDTH//2 + unit * UNIT_SIZE
            pygame.draw.line(screen, BLACK, (x_pos, HEIGHT//2 - 5), (x_pos, HEIGHT//2 + 5), 1)
            y_pos = HEIGHT//2 - unit * UNIT_SIZE
            pygame.draw.line(screen, BLACK, (WIDTH//2 - 5, y_pos), (WIDTH//2 + 5, y_pos), 1)

def Bresenham(x0, y0, x1, y1):
    pixels = []
    dx = x1 - x0
    dy = y1 - y0
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    
    if abs_dx >= abs_dy:
        err = 2 * abs_dy - abs_dx
        while True:
            pixels.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            if err >= 0:
                y0 += sy
                err += 2 * abs_dy - 2 * abs_dx
            else:
                err += 2 * abs_dy
            x0 += sx
    else:
        err = 2 * abs_dx - abs_dy
        while True:
            pixels.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            if err >= 0:
                x0 += sx
                err += 2 * abs_dx - 2 * abs_dy
            else:
                err += 2 * abs_dx
            y0 += sy
    
    return pixels

# Nét đứt: Lặp lại chu kỳ 10 pixel, vẽ pixel 1,2,3,4,5,6,7, bỏ pixel 8,9,10
def NetDut(x0, y0, x1, y1):
    pixels = Bresenham(x0, y0, x1, y1)
    for i, (x, y) in enumerate(pixels):
        position_in_cycle = (i % 10) + 1  # Vị trí trong chu kỳ 10 pixel (1-10)
        if position_in_cycle in [1, 2, 3, 4, 5, 6, 7]:  # Vẽ pixel 1,2,3,4,5,6,7
            pixel_x = WIDTH//2 + x * UNIT_SIZE
            pixel_y = HEIGHT//2 - y * UNIT_SIZE
            putPixel(pixel_x, pixel_y, x, y, RED)

# Nét chấm gạch: Lặp lại chu kỳ 10 pixel, vẽ pixel 1,2,3,4,5,8, bỏ pixel 6,7,9,10
def NetChamGach(x0, y0, x1, y1):
    pixels = Bresenham(x0, y0, x1, y1)
    for i, (x, y) in enumerate(pixels):
        position_in_cycle = (i % 10) + 1  # Vị trí trong chu kỳ 10 pixel (1-10)
        if position_in_cycle in [1, 2, 3, 4, 5, 8]:  # Vẽ pixel 1,2,3,4,5,8
            pixel_x = WIDTH//2 + x * UNIT_SIZE
            pixel_y = HEIGHT//2 - y * UNIT_SIZE
            putPixel(pixel_x, pixel_y, x, y, RED)

# Mũi tên: Vẽ đoạn thẳng AB và tam giác đều DEF tại B
def MuiTen(x0, y0, x1, y1):
    # Vẽ đoạn thẳng AB liên tục
    pixels = Bresenham(x0, y0, x1, y1)
    for x, y in pixels:
        pixel_x = WIDTH//2 + x * UNIT_SIZE
        pixel_y = HEIGHT//2 - y * UNIT_SIZE
        putPixel(pixel_x, pixel_y, x, y, RED)
    
    # Tính tam giác đều DEF ở điểm cuối (B)
    dx = x1 - x0
    dy = y1 - y0
    length = (dx**2 + dy**2)**0.5
    if length == 0:
        return
    
    # Vector đơn vị của AB
    dx_norm = dx / length
    dy_norm = dy / length
    
    # Độ dài cạnh tam giác đều
    c = 3  # Độ dài cạnh tam giác đều DEF
    # Tính tọa độ 3 đỉnh D, E, F dựa trên hướng của AB
    D = (x1 + (-dy_norm) * (c/2), y1 + dx_norm * (c/2))
    E = (x1 + dy_norm * (c/2), y1 + (-dx_norm) * (c/2))
    F = (x1 + dx_norm * (c * math.sqrt(3)/2), y1 + dy_norm * (c * math.sqrt(3)/2))
    
    # Vẽ tam giác DEF
    pixels_de = Bresenham(int(D[0]), int(D[1]), int(E[0]), int(E[1]))
    pixels_ef = Bresenham(int(E[0]), int(E[1]), int(F[0]), int(F[1]))
    pixels_fd = Bresenham(int(F[0]), int(F[1]), int(D[0]), int(D[1]))
    
    for x, y in pixels_de + pixels_ef + pixels_fd:
        pixel_x = WIDTH//2 + x * UNIT_SIZE
        pixel_y = HEIGHT//2 - y * UNIT_SIZE
        putPixel(pixel_x, pixel_y, x, y, RED)

# Hình chữ nhật: Vẽ từ 2 điểm trên đường chéo
def HinhChuNhat(x0, y0, x1, y1):
    # Tìm tọa độ 4 đỉnh của hình chữ nhật
    A = (x0, y0)
    B = (x1, y0)
    C = (x1, y1)
    D = (x0, y1)
    
    edges = [
        (A, B), (B, C), (C, D), (D, A)
    ]
    for (x0, y0), (x1, y1) in edges:
        pixels = Bresenham(x0, y0, x1, y1)
        for x, y in pixels:
            pixel_x = WIDTH//2 + x * UNIT_SIZE
            pixel_y = HEIGHT//2 - y * UNIT_SIZE
            putPixel(pixel_x, pixel_y, x, y, RED)

def add_points_from_input():
    try:
        # Ô nhập liệu thứ nhất: Điểm A (x0, y0)
        coords0 = input_texts[0].split(',')
        if len(coords0) == 2:
            x0 = int(coords0[0].strip())
            y0 = int(coords0[1].strip())
            points[0] = (x0, y0)
        else:
            return False

        # Ô nhập liệu thứ hai: Điểm B (x1, y1)
        coords1 = input_texts[1].split(',')
        if len(coords1) == 2:
            x1 = int(coords1[0].strip())
            y1 = int(coords1[1].strip())
            points[1] = (x1, y1)
        else:
            return False

        return True
    except ValueError:
        return False

def reset_inputs():
    """Reset tất cả các ô nhập liệu và điểm"""
    global input_texts, points
    input_texts = ["", ""]
    points = [None, None]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra nhấn vào các nút kiểu vẽ
            for mode, button in mode_buttons.items():
                if button.collidepoint(event.pos):
                    selected_mode = mode
                    # Giữ nguyên nhãn vì tất cả chế độ đều nhập 2 điểm
                    labels[1] = "B (x1,y1)"
                    break
            
            # Kiểm tra nhấn vào ô nhập liệu
            for i in range(2):
                if input_boxes[i].collidepoint(event.pos):
                    input_active[i] = True
                else:
                    input_active[i] = False
            
            # Kiểm tra nhấn nút OK
            if ok_button.collidepoint(event.pos):
                if add_points_from_input():
                    input_texts = ["", ""]
            
            # Kiểm tra nhấn nút Reset
            if reset_button.collidepoint(event.pos):
                reset_inputs()

        if event.type == pygame.KEYDOWN:
            for i in range(2):
                if input_active[i]:
                    if event.key == pygame.K_BACKSPACE:
                        input_texts[i] = input_texts[i][:-1]
                    else:
                        input_texts[i] += event.unicode

    draw_grid_and_axes()

    # Vẽ các nút kiểu vẽ
    for mode, button in mode_buttons.items():
        # Tô màu khác cho nút đang được chọn
        if mode == selected_mode:
            pygame.draw.rect(screen, DARK_GRAY, button, 0)
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, button, 0)
        pygame.draw.rect(screen, BLACK, button, 2)
        mode_text = font.render(mode, True, BLACK)
        screen.blit(mode_text, (button.x + 5, button.y + 5))

    # Vẽ ô nhập liệu và nút OK, Reset
    for i in range(2):
        pygame.draw.rect(screen, LIGHT_GRAY, input_boxes[i], 0)
        pygame.draw.rect(screen, BLACK, input_boxes[i], 2)
        display_text = input_texts[i] if input_texts[i] else (f"({points[i][0]},{points[i][1]})" if points[i] else "")
        label_text = f"{labels[i]}: {display_text}"
        input_surface = font.render(label_text, True, BLACK)
        screen.blit(input_surface, (input_boxes[i].x + 5, input_boxes[i].y + 5))

    pygame.draw.rect(screen, LIGHT_GRAY, ok_button, 0)
    pygame.draw.rect(screen, BLACK, ok_button, 2)
    ok_text = font.render("OK", True, BLACK)
    screen.blit(ok_text, (ok_button.x + 15, ok_button.y + 5))
    
    # Vẽ nút Reset
    pygame.draw.rect(screen, LIGHT_GRAY, reset_button, 0)
    pygame.draw.rect(screen, BLACK, reset_button, 2)
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(reset_text, (reset_button.x + 15, reset_button.y + 5))


    # Vẽ theo kiểu vẽ được chọn
    if points[0] and points[1]:
        x0, y0 = points[0]
        x1, y1 = points[1]
        
        if selected_mode == "Doan Thang":
            pixels = Bresenham(x0, y0, x1, y1)
            for x, y in pixels:
                pixel_x = WIDTH//2 + x * UNIT_SIZE
                pixel_y = HEIGHT//2 - y * UNIT_SIZE
                putPixel(pixel_x, pixel_y, x, y, RED)
        
        elif selected_mode == "Net Dut":
            NetDut(x0, y0, x1, y1)
        
        elif selected_mode == "Net Cham Gach":
            NetChamGach(x0, y0, x1, y1)
        
        elif selected_mode == "Mui Ten":
            MuiTen(x0, y0, x1, y1)
        
        elif selected_mode == "Hinh Chu Nhat":
            HinhChuNhat(x0, y0, x1, y1)

    pygame.display.flip()

pygame.quit()