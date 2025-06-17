import pygame
import math

# Cấu hình
WIDTH, HEIGHT = 800, 800
UNIT_SIZE = 5 # Số pixel đại diện 1 đơn vị
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (200, 200, 200)

# Khởi tạo
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vẽ đường tròn với thuật toán Bresenham")
font = pygame.font.SysFont('Arial', 12)

# Ô nhập liệu và nút OK, Reset
input_box = pygame.Rect(20, HEIGHT-80, 100, 30)  # Chỉ cần 1 ô nhập liệu cho bán kính R
ok_button = pygame.Rect(150, HEIGHT-80, 60, 30)
reset_button = pygame.Rect(230, HEIGHT-80, 80, 30)
input_text = ""  # Giá trị nhập vào (bán kính R)
input_active = False
R = None  # Giá trị bán kính sau khi nhấn OK

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

def BresenhamCircle(R):
    # Tính các điểm trong một octant (từ (0, R) đến khi x >= y)
    pixels = []
    x = 0
    y = R
    P = 3 - 2 * R  # Giá trị P ban đầu: P0 = 3 - 2R
    
    # Lặp đến khi x >= y (octant đầu tiên của góc phần tư thứ nhất)
    while x <= y:
        pixels.append((x, y))
        if P < 0:
            P = P + 4 * x + 6
        else:
            y -= 1
            P = P + 4 * (x - y) + 10
        x += 1
        
    return pixels

def VeNetDut(R):
    # Lấy danh sách các điểm trong một octant
    pixels = BresenhamCircle(R)
    
    # Áp dụng kiểu vẽ nét đứt và đối xứng 8 hướng
    for i, (x, y) in enumerate(pixels):
        position_in_cycle = (i % 8) + 1  # Vị trí trong chu kỳ 8 pixel (1-8)
        if position_in_cycle in [1, 2, 3, 4, 5]:  # Vẽ pixel 1,2,3,4,5
            # Tâm của hệ tọa độ trên màn hình là (WIDTH//2, HEIGHT//2)
            # Đối xứng 8 hướng
            # 1: (x, y)
            pixel_x = WIDTH//2 + x * UNIT_SIZE
            pixel_y = HEIGHT//2 - y * UNIT_SIZE
            putPixel(pixel_x, pixel_y, x, y, RED)
            
            # 2: (y, x)
            pixel_x = WIDTH//2 + y * UNIT_SIZE
            pixel_y = HEIGHT//2 - x * UNIT_SIZE
            putPixel(pixel_x, pixel_y, y, x, RED)
            
            # 3: (y, -x)
            pixel_x = WIDTH//2 + y * UNIT_SIZE
            pixel_y = HEIGHT//2 + x * UNIT_SIZE
            putPixel(pixel_x, pixel_y, y, -x, RED)
            
            # 4: (x, -y)
            pixel_x = WIDTH//2 + x * UNIT_SIZE
            pixel_y = HEIGHT//2 + y * UNIT_SIZE
            putPixel(pixel_x, pixel_y, x, -y, RED)
            
            # 5: (-x, -y)
            pixel_x = WIDTH//2 - x * UNIT_SIZE
            pixel_y = HEIGHT//2 + y * UNIT_SIZE
            putPixel(pixel_x, pixel_y, -x, -y, RED)
            
            # 6: (-y, -x)
            pixel_x = WIDTH//2 - y * UNIT_SIZE
            pixel_y = HEIGHT//2 + x * UNIT_SIZE
            putPixel(pixel_x, pixel_y, -y, -x, RED)
            
            # 7: (-y, x)
            pixel_x = WIDTH//2 - y * UNIT_SIZE
            pixel_y = HEIGHT//2 - x * UNIT_SIZE
            putPixel(pixel_x, pixel_y, -y, x, RED)
            
            # 8: (-x, y)
            pixel_x = WIDTH//2 - x * UNIT_SIZE
            pixel_y = HEIGHT//2 - y * UNIT_SIZE
            putPixel(pixel_x, pixel_y, -x, y, RED)

def add_radius_from_input():
    global R
    try:
        R = int(input_text.strip())
        if R <= 0:
            return False
        return True
    except ValueError:
        return False

def reset_inputs():
    global input_text, R
    input_text = ""
    R = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra nhấn vào ô nhập liệu
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
            
            # Kiểm tra nhấn nút OK
            if ok_button.collidepoint(event.pos):
                if add_radius_from_input():
                    input_text = ""
            
            # Kiểm tra nhấn nút Reset
            if reset_button.collidepoint(event.pos):
                reset_inputs()

        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    draw_grid_and_axes()

    # Vẽ ô nhập liệu và nút OK, Reset
    pygame.draw.rect(screen, LIGHT_GRAY, input_box, 0)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    display_text = input_text if input_text else (str(R) if R is not None else "")
    label_text = f"Bán kính (R): {display_text}"
    input_surface = font.render(label_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

    pygame.draw.rect(screen, LIGHT_GRAY, ok_button, 0)
    pygame.draw.rect(screen, BLACK, ok_button, 2)
    ok_text = font.render("OK", True, BLACK)
    screen.blit(ok_text, (ok_button.x + 15, ok_button.y + 5))
    
    pygame.draw.rect(screen, LIGHT_GRAY, reset_button, 0)
    pygame.draw.rect(screen, BLACK, reset_button, 2)
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(reset_text, (reset_button.x + 15, reset_button.y + 5))

    # Vẽ đường tròn nếu đã có bán kính R
    if R is not None:
        VeNetDut(R)

    pygame.display.flip()

pygame.quit()