# 游戏循环、事件监听、绘图调用
import pygame

# 小球参数
BALL_RADIUS = 20
BALL_COLOR = (255, 0, 0)

# 绳子挂点（固定）
ROPE_ORIGIN = (400, 100)

# 小球初始位置
ball_pos = (ROPE_ORIGIN[0], ROPE_ORIGIN[1] + 200)

pygame.init()

# 创建窗口，宽度800像素，高度600像素
screen = pygame.display.set_mode((800, 600))
# 设置窗口标题
pygame.display.set_caption("SwingBallGame")

# 游戏主循环
running = True
# 是否正在拖拽小球
dragging = False
print("程序开始")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 鼠标按下，检查是否点击在小球上
            mouse_x, mouse_y = event.pos
            # 判断是否在小球上
            dx = mouse_x - ball_pos[0]
            dy = mouse_y - ball_pos[1]
            if dx * dx + dy * dy <= BALL_RADIUS * BALL_RADIUS:
                dragging = True # 开始拖拽
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # 鼠标移动时，更新小球位置
                ball_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            print("鼠标松开")
            dragging = False  # 鼠标松开，停止拖拽
        
    
    # 窗口背景填充为白色
    screen.fill((255, 255, 255))
    # 绘制绳子
    pygame.draw.line(screen, (0, 0, 0), ROPE_ORIGIN, ball_pos, 2)
    # 绘制小球
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_RADIUS)
    # 将所有绘制更新到屏幕
    pygame.display.flip()
    # Ans:如果写在for内部，那么每处理一个事件就会刷新一次屏幕

# 释放Pygame资源
pygame.quit()