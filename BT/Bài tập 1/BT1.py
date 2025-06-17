import pygame

# Cấu hình
WIDTH, HEIGHT = 500, 500
UNIT_SIZE = 5
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

selected_pixels = []
input_active = False
input_text = ""
input_box = pygame.Rect(20, HEIGHT-40, 100, 30)  # Ô nhập liệu

def putPixel(pixel_x, pixel_y, x, y, color=RED):
    pygame.draw.rect(screen, color, 
                   (pixel_x - UNIT_SIZE//2,
                    pixel_y - UNIT_SIZE//2,
                    UNIT_SIZE, UNIT_SIZE))
    
    coord_text = font.render(f"({x}, {y})", True, BLACK)
    screen.blit(coord_text, (pixel_x + UNIT_SIZE//2, pixel_y))

def draw_grid_and_axes():
    screen.fill(WHITE)
    
    # Lưới và trục
    # for x in range(0, WIDTH, UNIT_SIZE):
    #     pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT))
    # for y in range(0, HEIGHT, UNIT_SIZE):
    #     pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y))
    
    pygame.draw.line(screen, BLACK, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2) #vẽ Ox
    pygame.draw.line(screen, BLACK, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2) #vẽ Oy
    
    for unit in range(-WIDTH//2//UNIT_SIZE, WIDTH//2//UNIT_SIZE + 1):
        if unit != 0:
            x_pos = WIDTH//2 + unit * UNIT_SIZE
            pygame.draw.line(screen, BLACK, (x_pos, HEIGHT//2 - 5), (x_pos, HEIGHT//2 + 5), 1)
            y_pos = HEIGHT//2 - unit * UNIT_SIZE
            pygame.draw.line(screen, BLACK, (WIDTH//2 - 5, y_pos), (WIDTH//2 + 5, y_pos), 1)

def add_point_from_input():
    try:
        coords = input_text.split(',')
        if len(coords) == 2:
            x = int(coords[0].strip())
            y = int(coords[1].strip())
            pixel_x = WIDTH//2 + x * UNIT_SIZE
            pixel_y = HEIGHT//2 - y * UNIT_SIZE
            selected_pixels.append((pixel_x, pixel_y, x, y))
            return True
    except ValueError:
        pass
    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra click vào ô input
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
                # Xử lý click chọn điểm
                mouse_x, mouse_y = event.pos
                x = round((mouse_x - WIDTH//2) / UNIT_SIZE)
                y = round((HEIGHT//2 - mouse_y) / UNIT_SIZE)
                pixel_x = WIDTH//2 + x * UNIT_SIZE
                pixel_y = HEIGHT//2 - y * UNIT_SIZE
                selected_pixels.append((pixel_x, pixel_y, x, y))
        
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    if add_point_from_input():
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    
    draw_grid_and_axes()
    
    # Vẽ các điểm
    for px, py, x, y in selected_pixels:
        putPixel(px, py, x, y)
    
    # Vẽ ô nhập liệu (góc trái dưới)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))
    
    # Hướng dẫn phía trên ô input
    help_text = font.render("Moi ban nhap toa do (x,y) roi Enter", True, BLACK)
    screen.blit(help_text, (20, HEIGHT-60))
    
    pygame.display.flip()

pygame.quit()