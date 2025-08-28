# 游戏循环、事件监听、绘图调用
import pygame
import math
import random

# 参数
BALL_RADIUS = 20
BALL_COLOR = (250, 100, 100)
ROPE_ORIGIN = (400, 300) # 绳子挂点（固定）
ball_pos = (ROPE_ORIGIN[0], ROPE_ORIGIN[1] + 200) # 小球初始位置
ROPE_LENGTH = 200 # 绳子长度
angle = math.pi / 2 # 初始化角度（弧度制，0表示正下方）
angle_speed = 0 # 角速度
GRAVITY = 0.0015 # 重力加速度
BUTTON_RECT = pygame.Rect(680, 540, 100, 40)

target_angle = random.uniform(0, 2 * math.pi)
target_center_x = int(ROPE_ORIGIN[0] + ROPE_LENGTH * math.sin(target_angle))
target_center_y = int(ROPE_ORIGIN[1] + ROPE_LENGTH * math.cos(target_angle))
TARGET_SIZE = 60
TARGET_RECT = pygame.Rect(
    target_center_x - TARGET_SIZE // 2,
    target_center_y - TARGET_SIZE // 2,
    TARGET_SIZE, TARGET_SIZE
)
TARGET_COLOR = (100, 200, 120)

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SwingBallGame")

# 游戏主循环
running = True
dragging = False # 是否正在拖拽小球
released = False # 鼠标是否松开
hit = False # 是否击中目标

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos # 鼠标按下，检查是否点击在小球上
            dx = mouse_x - ball_pos[0] # 判断是否在小球上
            dy = mouse_y - ball_pos[1]
            if dx * dx + dy * dy <= BALL_RADIUS * BALL_RADIUS:
                dragging = True # 开始拖拽
                released = False
            elif BUTTON_RECT.collidepoint(mouse_x, mouse_y):
                angle = math.pi / 2
                angle_speed = 0
                ball_pos = (ROPE_ORIGIN[0], ROPE_ORIGIN[1] + ROPE_LENGTH)
                dragging = False
                released = False
                hit = False
                target_angle = random.uniform(0, 2 * math.pi)
                target_center_x = int(ROPE_ORIGIN[0] + ROPE_LENGTH * math.sin(target_angle))
                target_center_y = int(ROPE_ORIGIN[1] + ROPE_LENGTH * math.cos(target_angle))
                TARGET_RECT = pygame.Rect(
                    target_center_x - TARGET_SIZE // 2,
                    target_center_y - TARGET_SIZE // 2,
                    TARGET_SIZE, TARGET_SIZE
                )

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - ROPE_ORIGIN[0]
                dy = mouse_y - ROPE_ORIGIN[1]
                dist = math.hypot(dx, dy)
                if dist != ROPE_LENGTH:
                    scale = ROPE_LENGTH / dist
                    dx *= scale
                    dy *= scale
                    ball_pos = (int(ROPE_ORIGIN[0] + dx), int(ROPE_ORIGIN[1] + dy))
                else:
                    ball_pos = (mouse_x, mouse_y)
                angle = math.atan2(dx, dy)
                angle_speed = 0  # 拖拽时速度清零

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                released = True
            else:
                dragging = False
    
    # 没有拖拽时，进行物理模拟
    if released and not dragging:
        # 计算角速度 -g/L * sin(angle)
        angle_acc = -GRAVITY / ROPE_LENGTH * math.sin(angle)
        angle_speed += angle_acc
        angle_speed *= 0.99995 # 阻尼
        angle += angle_speed
        # 根据角度计算小球位置
        ball_pos = (
            int (ROPE_ORIGIN[0] + ROPE_LENGTH * math.sin(angle)),
            int (ROPE_ORIGIN[1] + ROPE_LENGTH * math.cos(angle))
        )

    if not hit:
        nearest_x = max(TARGET_RECT.left, min(ball_pos[0], TARGET_RECT.right))
        nearest_y = max(TARGET_RECT.top, min(ball_pos[1], TARGET_RECT.bottom))
        dist_to_rect = math.hypot(ball_pos[0] - nearest_x, ball_pos[1] - nearest_y)
        if dist_to_rect <= BALL_RADIUS:
            hit = True

    # 绘图
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (120, 180, 220), BUTTON_RECT)
    font = pygame.font.SysFont(None, 28)
    text = font.render("action", True, (30, 30, 30))
    screen.blit(text, (BUTTON_RECT.x + 25, BUTTON_RECT.y + 8))
    pygame.draw.line(screen, (0, 0, 0), ROPE_ORIGIN, ball_pos, 2)
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_RADIUS)
    pygame.draw.rect(screen, TARGET_COLOR, TARGET_RECT)
    if hit:
        pygame.draw.rect(screen, (200, 80, 80), TARGET_RECT)
    else:
        pygame.draw.rect(screen, TARGET_COLOR, TARGET_RECT)
    pygame.display.flip()
    # Ans:如果写在for内部，那么每处理一个事件就会刷新一次屏幕

pygame.quit()