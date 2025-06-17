import pygame

# Cấu hình
WIDTH, HEIGHT = 800, 800
UNIT_SIZE = 5 # Số pixel đại diện 1 đơn vị
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Màu xanh cho elip
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (200, 200, 200)

# Khởi tạo
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vẽ hình elip với thuật toán Midpoint")
font = pygame.font.SysFont('Arial', 12)

# Ô nhập liệu và nút OK, Reset
input_box_a = pygame.Rect(20, HEIGHT-80, 100, 30)  # Ô nhập liệu cho a
input_box_b = pygame.Rect(130, HEIGHT-80, 100, 30)  # Ô nhập liệu cho b
ok_button = pygame.Rect(250, HEIGHT-80, 60, 30)
reset_button = pygame.Rect(330, HEIGHT-80, 80, 30)
input_text_a = ""  # Giá trị nhập vào cho a
input_text_b = ""  # Giá trị nhập vào cho b
input_active_a = False
input_active_b = False
a = None  # Giá trị a sau khi nhấn OK
b = None  # Giá trị b sau khi nhấn OK

def putPixel(pixel_x, pixel_y, x, y, color=BLUE):
    pygame.draw.rect(screen, color, 
                   (pixel_x - UNIT_SIZE//2,
                    pixel_y - UNIT_SIZE//2,
                    UNIT_SIZE, UNIT_SIZE))
    """ Kiểm tra tọa độ
    coord_text = font.render(f"({x}, {y})", True, BLACK)
    screen.blit(coord_text, (pixel_x + UNIT_SIZE//2, pixel_y))
    """

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

def MidpointEllipse(a, b):
    pixels = []
    
    # Phần I: Tăng x, điều chỉnh y
    x = 0
    y = b
    P = b**2 - a**2 * b + (a**2) // 4  # Giá trị P ban đầu
    
    while b**2 * x <= a**2 * y:  # Điều kiện dừng: b^2*x > a^2*y (độ dốc -1)
        pixels.append((x, y))
        if P < 0:
            P = P + b**2 * (2 * x + 3)
        else:
            P = P + b**2 * (2 * x + 3) + a**2 * (-2 * y + 2)
            y -= 1
        x += 1
    
    # Phần II: Giảm y, điều chỉnh x
    Q = b**2 * (x + 0.5)**2 + a**2 * (y - 1)**2 - a**2 * b**2  # Giá trị Q ban đầu
    while y >= 0:  # Điều kiện dừng: y < 0
        pixels.append((x, y))
        if Q < 0:
            Q = Q + b**2 * (2 * x + 2) + a**2 * (-2 * y + 3)
            x += 1
        else:
            Q = Q + a**2 * (-2 * y + 3)
        y -= 1
    
    return pixels

def veNetDut(a, b):
    # Lấy danh sách các điểm trong góc phần tư thứ nhất
    pixels = MidpointEllipse(a, b)
    
    # Áp dụng kiểu vẽ nét đứt cho nửa trên và nét liền cho nửa dưới
    for i, (x, y) in enumerate(pixels):
        # Đối xứng 4 hướng
        points = [
            (x, y),   # Góc phần tư thứ nhất
            (-x, y),  # Góc phần tư thứ hai
            (-x, -y), # Góc phần tư thứ ba
            (x, -y)   # Góc phần tư thứ tư
        ]
        
        for px, py in points:
            pixel_x = WIDTH//2 + px * UNIT_SIZE
            pixel_y = HEIGHT//2 - py * UNIT_SIZE
            
            # Nửa trên (y >= 0): Nét đứt (chu kỳ 8 ô: vẽ 5 ô, bỏ 3 ô)
            if py >= 0:
                position_in_cycle = (i % 8) + 1  # Vị trí trong chu kỳ 8 pixel (1-8)
                if position_in_cycle in [1, 2, 3, 4, 5]:  # Vẽ pixel 1,2,3,4,5
                    putPixel(pixel_x, pixel_y, px, py, BLUE)
            # Nửa dưới (y < 0): Nét liền
            else:
                putPixel(pixel_x, pixel_y, px, py, BLUE)

def add_axes_from_input():
    global a, b
    try:
        a_val = int(input_text_a.strip())
        b_val = int(input_text_b.strip())
        if a_val <= 0 or b_val <= 0:
            return False
        a, b = a_val, b_val
        return True
    except ValueError:
        return False

def reset_inputs():
    global input_text_a, input_text_b, a, b
    input_text_a = ""
    input_text_b = ""
    a = None
    b = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra nhấn vào ô nhập liệu cho a
            if input_box_a.collidepoint(event.pos):
                input_active_a = True
                input_active_b = False
            # Kiểm tra nhấn vào ô nhập liệu cho b
            elif input_box_b.collidepoint(event.pos):
                input_active_a = False
                input_active_b = True
            else:
                input_active_a = False
                input_active_b = False
            
            # Kiểm tra nhấn nút OK
            if ok_button.collidepoint(event.pos):
                if add_axes_from_input():
                    input_text_a = ""
                    input_text_b = ""
            
            # Kiểm tra nhấn nút Reset
            if reset_button.collidepoint(event.pos):
                reset_inputs()

        if event.type == pygame.KEYDOWN:
            if input_active_a:
                if event.key == pygame.K_BACKSPACE:
                    input_text_a = input_text_a[:-1]
                else:
                    input_text_a += event.unicode
            elif input_active_b:
                if event.key == pygame.K_BACKSPACE:
                    input_text_b = input_text_b[:-1]
                else:
                    input_text_b += event.unicode

    draw_grid_and_axes()

    # Vẽ ô nhập liệu và nút OK, Reset
    # Ô nhập liệu cho a
    pygame.draw.rect(screen, LIGHT_GRAY, input_box_a, 0)
    pygame.draw.rect(screen, BLACK, input_box_a, 2)
    display_text_a = input_text_a if input_text_a else (str(a) if a is not None else "")
    label_text_a = f"a: {display_text_a}"
    input_surface_a = font.render(label_text_a, True, BLACK)
    screen.blit(input_surface_a, (input_box_a.x + 5, input_box_a.y + 5))

    # Ô nhập liệu cho b
    pygame.draw.rect(screen, LIGHT_GRAY, input_box_b, 0)
    pygame.draw.rect(screen, BLACK, input_box_b, 2)
    display_text_b = input_text_b if input_text_b else (str(b) if b is not None else "")
    label_text_b = f"b: {display_text_b}"
    input_surface_b = font.render(label_text_b, True, BLACK)
    screen.blit(input_surface_b, (input_box_b.x + 5, input_box_b.y + 5))

    # Nút OK
    pygame.draw.rect(screen, LIGHT_GRAY, ok_button, 0)
    pygame.draw.rect(screen, BLACK, ok_button, 2)
    ok_text = font.render("OK", True, BLACK)
    screen.blit(ok_text, (ok_button.x + 15, ok_button.y + 5))
    
    # Nút Reset
    pygame.draw.rect(screen, LIGHT_GRAY, reset_button, 0)
    pygame.draw.rect(screen, BLACK, reset_button, 2)
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(reset_text, (reset_button.x + 15, reset_button.y + 5))

    # Vẽ elip nếu đã có a và b
    if a is not None and b is not None:
        veNetDut(a, b)

    pygame.display.flip()

pygame.quit()