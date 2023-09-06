import pygame
import math
from copy import copy

pygame.init()

# Увеличиваем размер экрана
WIN_WIDTH = int(1000 * 1.2)
WIN_HEIGHT = int(800 * 1.2)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

SCALE_FACTOR = 1.2

# Увеличиваем размер изображений
body = pygame.transform.scale(pygame.image.load('body.svg').convert_alpha(), 
                              (int(pygame.image.load('body.svg').get_width() * SCALE_FACTOR),
                               int(pygame.image.load('body.svg').get_height() * SCALE_FACTOR)))
boom = pygame.transform.scale(pygame.image.load('boom.svg').convert(), 
                              (int(pygame.image.load('boom.svg').get_width() * SCALE_FACTOR),
                               int(pygame.image.load('boom.svg').get_height() * SCALE_FACTOR)))
arm = pygame.transform.scale(pygame.image.load('arm.svg').convert(), 
                             (int(pygame.image.load('arm.svg').get_width() * SCALE_FACTOR),
                              int(pygame.image.load('arm.svg').get_height() * SCALE_FACTOR)))
bucket = pygame.transform.scale(pygame.image.load('bucket.svg').convert(), 
                               (int(pygame.image.load('bucket.svg').get_width() * SCALE_FACTOR),
                                int(pygame.image.load('bucket.svg').get_height() * SCALE_FACTOR)))
big_bucket = pygame.image.load('bucket.png').convert()

body.set_colorkey((255, 255, 255))
boom.set_colorkey((255, 255, 255))
arm.set_colorkey((255, 255, 255))
bucket.set_colorkey((255, 255, 255))
big_bucket.set_colorkey((255, 255, 255))

# Увеличиваем координаты начального положения
fang_initial = (int(146 * SCALE_FACTOR), int(34 * SCALE_FACTOR))
boom_anchor_img = (int(238 * SCALE_FACTOR), int(130 * SCALE_FACTOR))
boom_anchor = (int(378 * SCALE_FACTOR), int(367 * SCALE_FACTOR))

arm_anchor_img = (int(146 * SCALE_FACTOR), int(73 * SCALE_FACTOR))
arm_pivot = (int(277 * SCALE_FACTOR), int(154 * SCALE_FACTOR))
bucket_position = [int(111 * SCALE_FACTOR), int(26 * SCALE_FACTOR)]
bucket_pivot = (int(161 * SCALE_FACTOR), int(92 * SCALE_FACTOR))
body_x = int(300 * SCALE_FACTOR)
body_y = int(300 * SCALE_FACTOR)

# ... (остальная часть кода остается прежней)


prev_body_x = body_x
prev_body_y = body_y
bucket_angle = 0
arm_angle = 0
boom_angle = 0
pygame.font.init()
font = pygame.font.SysFont(None, 36)  # Выберите шрифт и размер на свой вкус

slider_bucket = [0, 660, 1200]  # x, y, длина
slider_arm = [0, 530, 1200]
slider_boom = [0, 590, 1200]

# Определите начальные скорости (конечные значения будут зависеть от положения ползунка)
speed_bucket = 0
speed_arm = 0
speed_boom = 0
scale_factor = 1

def blitRotateCenter(win, image, top_left, angle, pivot):
    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=pivot)
    win.blit(rotated_image, rect.topleft)
    return rect

def rotate_point_around_point(px, py, cx, cy, angle):
    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))

    # Перемещение точки в начало координат
    px -= cx
    py -= cy

    # Примените поворот
    x_new = px * c - py * s
    y_new = px * s + py * c

    # Верните точку обратно
    x_new += cx
    y_new += cy

    return x_new, y_new

run = True
prev_keys = pygame.key.get_pressed()
body_rotation_angle = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)

    
    pygame.draw.rect(win, (0, 0, 255), (slider_bucket[0], slider_bucket[1], slider_bucket[2], 20))
    pygame.draw.rect(win, (0, 255, 0), (slider_arm[0], slider_arm[1], slider_arm[2], 20))
    pygame.draw.rect(win, (255, 0, 0), (slider_boom[0], slider_boom[1], slider_boom[2], 20))
    # Управление скоростью
    keys = pygame.key.get_pressed()

    just_pressed_RIGHT = keys[pygame.K_RIGHT] and not prev_keys[pygame.K_RIGHT]
    just_pressed_LEFT = keys[pygame.K_LEFT] and not prev_keys[pygame.K_LEFT]
    just_pressed_UP = keys[pygame.K_UP] and not prev_keys[pygame.K_UP]
    just_pressed_DOWN = keys[pygame.K_DOWN] and not prev_keys[pygame.K_DOWN]
    just_pressed_w = keys[pygame.K_w] and not prev_keys[pygame.K_w]
    just_pressed_s = keys[pygame.K_s] and not prev_keys[pygame.K_s]
    
    if keys[pygame.K_a]:
        body_x -= 0.3  
    if keys[pygame.K_d]:
        body_x += 0.3
    delta_x = body_x - prev_body_x
    delta_y = body_y - prev_body_y
    boom_anchor  = (boom_anchor[0] + delta_x, boom_anchor[1] + delta_y)
    arm_pivot = (arm_pivot[0] + delta_x, arm_pivot[1] + delta_y)
    bucket_pivot = (bucket_pivot[0] + delta_x, bucket_pivot[1] + delta_y)
        

    prev_body_x = body_x
    prev_body_y = body_y
  
    # Управление скоростью для ковша
    if just_pressed_RIGHT:
        if speed_bucket > 0:
            speed_bucket = 0

        else:
            speed_bucket -= 0.05

    if just_pressed_LEFT:
        if speed_bucket < 0:
            speed_bucket = 0

        else:
            speed_bucket += 0.05

    # Управление скоростью для рукояти
    if just_pressed_w:
        if speed_arm > 0:
            speed_arm = 0

        else:
            speed_arm -= 0.01

    if just_pressed_s:
        if speed_arm < 0:
            speed_arm = 0

        else:
            speed_arm += 0.01

    # Управление скоростью для стрелы
    if just_pressed_DOWN:
        if speed_boom > 0:
            speed_boom = 0

        else:
            speed_boom -= 0.01

    if just_pressed_UP:
        if speed_boom < 0:
            speed_boom = 0

        else:
            speed_boom += 0.01


    # Применение скорости к углам
    bucket_angle += speed_bucket
    arm_angle += speed_arm
    boom_angle += speed_boom
    

    # Ограничения углов
    if not (0 <= bucket_angle <= 180):
        bucket_angle = max(0, min(180, bucket_angle))
        speed_bucket = 0

    if not (0 <= arm_angle <= 120):
        arm_angle = max(0, min(120, arm_angle))
        speed_arm = 0

    if not (0 <= boom_angle <= 112):
        boom_angle = max(0, min(112, boom_angle))
        speed_boom = 0





    
    win.fill((255, 255, 255))
    # bucket_text = font.render('Угол ковша: {:.2f}'.format(bucket_angle), True, (0, 0, 0))
    # arm_text = font.render('Угол рукояти: {:.2f}'.format(arm_angle), True, (0, 0, 0))
    # boom_text = font.render('Угол стрелы: {:.2f}'.format(boom_angle), True, (0, 0, 0))
    

    win.blit(body, (body_x, body_y))
    pygame.draw.rect(win, (0, 0, 255), (slider_bucket[0], slider_bucket[1], slider_bucket[2], 20))
    pygame.draw.rect(win, (0, 255, 0), (slider_arm[0], slider_arm[1], slider_arm[2], 20))
    pygame.draw.rect(win, (255, 0, 0), (slider_boom[0], slider_boom[1], slider_boom[2], 20))   
    # win.blit(bucket_text, (WIN_WIDTH - bucket_text.get_width() - 10, 10))
    # win.blit(arm_text, (WIN_WIDTH - arm_text.get_width() - 10, 50))
    # win.blit(boom_text, (WIN_WIDTH - boom_text.get_width() - 10, 90))

    ######################
    #####################
    #####################
    # Поворачиваем стрелу
    blitRotateCenter(win, boom, boom_anchor_img, boom_angle, boom_anchor)

    # Рассчитываем новое положение для arm_pivot после поворота стрелы
    dist_to_arm = math.sqrt((arm_pivot[0] - boom_anchor[0]) ** 2 + (arm_pivot[1] - boom_anchor[1]) ** 2)
    angle_to_arm = math.atan2(boom_anchor[1] - arm_pivot[1], arm_pivot[0] - boom_anchor[0])
    new_arm_pivot_x = boom_anchor[0] + dist_to_arm * math.cos(angle_to_arm + math.radians(boom_angle))
    new_arm_pivot_y = boom_anchor[1] - dist_to_arm * math.sin(angle_to_arm + math.radians(boom_angle))

    # Поворачиваем рукоять вокруг новой опорной точки
    arm_position = blitRotateCenter(win, arm, (new_arm_pivot_x - arm_anchor_img[0], new_arm_pivot_y - arm_anchor_img[1]), boom_angle + arm_angle, (new_arm_pivot_x, new_arm_pivot_y))

    # Рассчитываем новое положение для bucket_pivot после поворота рукояти
    dist_to_bucket_from_new_arm = math.sqrt((bucket_pivot[0] - arm_pivot[0]) ** 2 + (bucket_pivot[1] - arm_pivot[1]) ** 2)
    angle_to_bucket_from_new_arm = math.atan2(arm_pivot[1] - bucket_pivot[1], bucket_pivot[0] - arm_pivot[0])
    new_bucket_pivot_x = new_arm_pivot_x + dist_to_bucket_from_new_arm * math.cos(angle_to_bucket_from_new_arm + math.radians(boom_angle + arm_angle))
    new_bucket_pivot_y = new_arm_pivot_y - dist_to_bucket_from_new_arm * math.sin(angle_to_bucket_from_new_arm + math.radians(boom_angle + arm_angle))

    fang_x = new_bucket_pivot_x + (fang_initial[0] - bucket_position[0]) * math.cos(math.radians(boom_angle + arm_angle + bucket_angle)) - (fang_initial[1] - bucket_position[1]) * math.sin(math.radians(boom_angle + arm_angle + bucket_angle))
    fang_y = new_bucket_pivot_y + (fang_initial[0] - bucket_position[0]) * math.sin(math.radians(boom_angle + arm_angle + bucket_angle)) + (fang_initial[1] - bucket_position[1]) * math.cos(math.radians(boom_angle + arm_angle + bucket_angle))
    # Поворачиваем ковш вокруг новой опорной точки
    blitRotateCenter(win, bucket, (new_bucket_pivot_x - bucket_position[0], new_bucket_pivot_y - bucket_position[1]), boom_angle + arm_angle + bucket_angle, (new_bucket_pivot_x, new_bucket_pivot_y))
    blitRotateCenter(win, big_bucket, (890, 350), boom_angle + arm_angle + bucket_angle, (890, 350))
    #####################
    #####################
    #####################
    arm_delta_x = new_bucket_pivot_x - new_arm_pivot_x
    arm_delta_y = new_bucket_pivot_y - new_arm_pivot_y
    bucket_delta_y = new_bucket_pivot_y - fang_y
    bucket_delta_x = new_bucket_pivot_x - fang_x

    bucket_angle_from_horizontal = 90 + math.degrees(math.atan2(bucket_delta_y, bucket_delta_x))

    arm_angle_from_horizontal = math.degrees(math.atan2(arm_delta_y, -arm_delta_x))

    # arm_text_from_horizontal = font.render('Угол рукояти отн. горизонта: {:.2f}'.format(arm_angle_from_horizontal), True, (0, 0, 0))
    # bucket_text_from_horizontal = font.render('Угол ковша отн. горизонта: {:.2f}'.format(bucket_angle_from_horizontal), True, (0, 0, 0))
    # win.blit(arm_text_from_horizontal, (10, 10))
    # win.blit(bucket_text_from_horizontal, (10, 35))

    prev_keys = copy(keys)
    pygame.display.update()

pygame.quit()



'''
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)

'''