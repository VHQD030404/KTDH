# Import thư viện Pygame để xử lý đồ họa và sự kiện
import pygame
# Import các hàm vẽ từ file drawing.py
from drawing import draw_grid, draw_axes_2d, midpoint_line, draw_circle, draw_axes_3d, draw_cube

# Khởi tạo Pygame, thiết lập các thành phần cần thiết (hiển thị, sự kiện, v.v.)
pygame.init()
# Định nghĩa kích thước cửa sổ: rộng 800px, cao 600px
WIDTH, HEIGHT = 800, 600
# Định nghĩa kích thước nút bấm: rộng 100px, cao 40px
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
# Tạo cửa sổ Pygame với kích thước đã định
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Đặt tiêu đề cửa sổ
pygame.display.set_caption("Simple Drawing App")
# Tạo đối tượng Clock để giới hạn tốc độ khung hình (FPS)
clock = pygame.time.Clock()

# Trạng thái ứng dụng, lưu thông tin về chế độ vẽ, hình, màu, v.v.
state = {
    "mode": "2D",            # Chế độ hiện tại: "2D" hoặc "3D"
    "shape": "line",         # Hình được chọn: "line", "circle", hoặc "cube"
    "color": (255, 0, 0),    # Màu vẽ: RGB, mặc định là đỏ
    "grid_size": 5,          # Kích thước ô lưới: 5 pixel
    "drawing": False,        # Trạng thái đang vẽ (khi nhấn chuột)
    "start_pos": None,       # Tọa độ bắt đầu khi vẽ (x, y)
    "end_pos": None          # Tọa độ kết thúc khi vẽ (x, y)
}

# Định nghĩa danh sách các nút bấm, mỗi nút có nhãn, vị trí, và hành động
buttons = [
    # Nút "2D Mode": chuyển sang chế độ 2D
    {"label": "2D Mode", "rect": pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT), "action": lambda: update_state(mode="2D")},
    # Nút "3D Mode": chuyển sang chế độ 3D
    {"label": "3D Mode", "rect": pygame.Rect(10, 60, BUTTON_WIDTH, BUTTON_HEIGHT), "action": lambda: update_state(mode="3D")},
    # Nút "Line": chọn vẽ đoạn thẳng
    {"label": "Line", "rect": pygame.Rect(10, 110, BUTTON_WIDTH, BUTTON_HEIGHT), "action": lambda: update_state(shape="line")},
    # Nút "Circle": chọn vẽ hình tròn
    {"label": "Circle", "rect": pygame.Rect(10, 160, BUTTON_WIDTH, BUTTON_HEIGHT), "action": lambda: update_state(shape="circle")},
    # Nút "Cube": chọn vẽ hình hộp
    {"label": "Cube", "rect": pygame.Rect(10, 210, BUTTON_WIDTH, BUTTON_HEIGHT), "action": lambda: update_state(shape="cube")},
    # Nút "Red": chọn màu đỏ
    {"label": "Red", "rect": pygame.Rect(10, 260, BUTTON_WIDTH, BUTTON_HEIGHT), "action": lambda: update_state(color=(255, 0, 0))},
    # Nút "Blue": chọn màu xanh dương
    {"label": "Blue", "rect": pygame.Rect(10, 310, BUTTON_WIDTH, BUTTON_HEIGHT), "action": lambda: update_state(color=(0, 0, 255))}
]

# Hàm khởi tạo font chữ để hiển thị nhãn nút
def setup():
    # Khởi tạo hệ thống font của Pygame
    pygame.font.init()
    # Định nghĩa biến font toàn cục, sử dụng font Arial kích thước 20
    global font
    font = pygame.font.SysFont("arial", 20)

# Hàm vẽ các nút bấm lên màn hình
def draw_buttons(surface):
    # Duyệt qua từng nút trong danh sách
    for button in buttons:
        # Vẽ hình chữ nhật màu xám nhạt cho nút
        pygame.draw.rect(surface, (200, 200, 200), button["rect"])
        # Tạo văn bản từ nhãn của nút, màu đen
        text = font.render(button["label"], True, (0, 0, 0))
        # Vẽ văn bản lên màn hình, căn lề trong nút
        surface.blit(text, (button["rect"].x + 10, button["rect"].y + 10))

# Hàm cập nhật trạng thái ứng dụng
def update_state(mode=None, shape=None, color=None):
    # Cập nhật chế độ nếu được cung cấp
    if mode:
        state["mode"] = mode
    # Cập nhật hình vẽ nếu được cung cấp
    if shape:
        state["shape"] = shape
    # Cập nhật màu nếu được cung cấp
    if color:
        state["color"] = color

# Hàm cập nhật và vẽ toàn bộ cảnh (scene)
def update_scene(surface):
    # Xóa màn hình, tô màu trắng
    surface.fill((255, 255, 255))
    # Vẽ các nút bấm
    draw_buttons(surface)
    
    # Định nghĩa khu vực vẽ (bên phải nút bấm)
    draw_area = pygame.Rect(BUTTON_WIDTH + 20, 10, WIDTH - BUTTON_WIDTH - 30, HEIGHT - 20)
    # Vẽ nền xám nhạt cho khu vực vẽ
    pygame.draw.rect(surface, (220, 220, 220), draw_area)
    
    # Nếu ở chế độ 2D
    if state["mode"] == "2D":
        # Vẽ lưới pixel
        draw_grid(surface, state["grid_size"], draw_area)
        # Vẽ hệ trục tọa độ 2D
        draw_axes_2d(surface, draw_area)
        # Nếu đang vẽ đoạn thẳng và có điểm bắt đầu/kết thúc
        if state["shape"] == "line" and state["start_pos"] and state["end_pos"]:
            # Vẽ đoạn thẳng bằng thuật toán Midpoint
            midpoint_line(surface, state["start_pos"][0], state["start_pos"][1], 
                         state["end_pos"][0], state["end_pos"][1], state["color"])
        # Nếu đang vẽ hình tròn và có điểm bắt đầu/kết thúc
        elif state["shape"] == "circle" and state["start_pos"] and state["end_pos"]:
            # Tính bán kính từ khoảng cách hai điểm
            radius = int(((state["end_pos"][0] - state["start_pos"][0])**2 + 
                         (state["end_pos"][1] - state["start_pos"][1])**2)**0.5)
            # Vẽ hình tròn
            draw_circle(surface, state["start_pos"][0], state["start_pos"][1], radius, state["color"])
    # Nếu ở chế độ 3D
    else:
        # Vẽ hệ trục tọa độ 3D
        draw_axes_3d(surface, draw_area)
        # Nếu chọn vẽ hình hộp
        if state["shape"] == "cube":
            # Định nghĩa 8 đỉnh của hình hộp
            vertices = [(50, 50, 50), (50, 50, -50), (50, -50, 50), (50, -50, -50),
                       (-50, 50, 50), (-50, 50, -50), (-50, -50, 50), (-50, -50, -50)]
            # Vẽ hình hộp bằng phép chiếu cavalier
            draw_cube(surface, vertices, "cavalier", draw_area)

# Hàm xử lý sự kiện người dùng (chuột, thoát chương trình)
def handle_events():
    # Duyệt qua tất cả sự kiện Pygame
    for event in pygame.event.get():
        # Nếu người dùng đóng cửa sổ
        if event.type == pygame.QUIT:
            return False
        # Nếu nhấn chuột
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem có nhấn vào nút nào không
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    button["action"]()
            # Nếu nhấn trong khu vực vẽ
            if pygame.Rect(BUTTON_WIDTH + 20, 10, WIDTH - BUTTON_WIDTH - 30, HEIGHT - 20).collidepoint(event.pos):
                state["start_pos"] = event.pos
                state["drawing"] = True
        # Nếu di chuyển chuột trong khi nhấn
        elif event.type == pygame.MOUSEMOTION and state["drawing"]:
            state["end_pos"] = event.pos
        # Nếu thả chuột
        elif event.type == pygame.MOUSEBUTTONUP:
            state["drawing"] = False
    return True

# Hàm chính chạy chương trình
def main():
    # Khởi tạo font
    setup()
    # Biến kiểm soát vòng lặp chính
    running = True
    while running:
        # Xử lý sự kiện, thoát nếu trả về False
        running = handle_events()
        # Cập nhật và vẽ cảnh
        update_scene(screen)
        # Cập nhật màn hình
        pygame.display.flip()
        # Giới hạn 60 FPS
        clock.tick(60)

# Chạy chương trình nếu là file chính
if __name__ == "__main__":
    main()
    # Đóng Pygame khi thoát
    pygame.quit()