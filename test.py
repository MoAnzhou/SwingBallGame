import pygame
import sys

# 初始化 pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Demo 测试")

# 设置颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 小球初始位置
x, y = WIDTH // 2, HEIGHT // 2
radius = 30
speed_x, speed_y = 3, 3

# 游戏主循环
clock = pygame.time.Clock()
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新小球位置
    x += speed_x
    y += speed_y

    # 碰到边界反弹
    if x - radius < 0 or x + radius > WIDTH:
        speed_x = -speed_x
    if y - radius < 0 or y + radius > HEIGHT:
        speed_y = -speed_y

    # 绘制
    screen.fill(WHITE)  # 填充背景
    pygame.draw.circle(screen, RED, (x, y), radius)

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出 pygame
pygame.quit()
sys.exit()
