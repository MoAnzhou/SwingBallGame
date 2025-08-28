# 游戏循环、事件监听、绘图调用
import pygame
import math

# 参数
BALL_RADIUS = 20
BALL_COLOR = (250, 100, 100)
ROPE_ORIGIN = (400, 100) # 绳子挂点（固定）
ball_pos = (ROPE_ORIGIN[0], ROPE_ORIGIN[1] + 200) # 小球初始位置
ROPE_LENGTH = 200 # 绳子长度
angle = math.pi / 2 # 初始化角度（弧度制，0表示正下方）
angle_speed = 0 # 角速度
GRAVITY = 0.0015 # 重力加速度

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SwingBallGame")

# 游戏主循环
running = True
dragging = False # 是否正在拖拽小球
released = False # 鼠标是否松开

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
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                ball_pos = event.pos # 鼠标移动时，更新小球位置
                # 计算拖拽时的角度
                dx = ball_pos[0] - ROPE_ORIGIN[0]
                dy = ball_pos[1] - ROPE_ORIGIN[1]
                angle = math.atan2(dx, dy)
                angle_speed = 0  # 拖拽时速度清零
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            released = True
    
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

    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 0, 0), ROPE_ORIGIN, ball_pos, 2)
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_RADIUS)
    pygame.display.flip()
    # Ans:如果写在for内部，那么每处理一个事件就会刷新一次屏幕

pygame.quit()