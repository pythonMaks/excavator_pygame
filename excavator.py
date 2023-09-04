import pygame
import math

pygame.init()

win = pygame.display.set_mode((800, 600))

body = pygame.image.load('body.svg').convert_alpha()
body.set_colorkey((255, 255, 255))
boom = pygame.image.load('boom.svg').convert()
boom.set_colorkey((255, 255, 255))
arm = pygame.image.load('arm.svg').convert()
arm.set_colorkey((255, 255, 255))
bucket = pygame.image.load('bucket.svg').convert()
bucket.set_colorkey((255, 255, 255))

boom_anchor_img = (238, 130)
bucket_position = [114, 26]
boom_anchor  = (378, 367)
arm_anchor_img = (149, 73)
arm_pivot = (280, 154)
bucket_pivot = (164, 92)
bucket_angle = 0
arm_angle = 0

def blitRotateCenter(win, image, top_left, angle, pivot):
    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=pivot)
    win.blit(rotated_image, rect.topleft)
    return rect
boom_angle = 0
run = True
boom_angle = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and bucket_angle < 180:
        bucket_angle += 1
    if keys[pygame.K_d] and bucket_angle > 0:
        bucket_angle -= 1

    if keys[pygame.K_w] and arm_angle < 90:
        arm_angle += 1
    if keys[pygame.K_s] and arm_angle > 0:
        arm_angle -= 1

    if keys[pygame.K_LEFT] and boom_angle < 112:
        boom_angle += 1
    if keys[pygame.K_RIGHT] and boom_angle > 0:
        boom_angle -= 1
    
    win.fill((255, 255, 255))
    win.blit(body, (300, 300))
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

    # Поворачиваем ковш вокруг новой опорной точки
    blitRotateCenter(win, bucket, (new_bucket_pivot_x - bucket_position[0], new_bucket_pivot_y - bucket_position[1]), boom_angle + arm_angle + bucket_angle, (new_bucket_pivot_x, new_bucket_pivot_y))

    pygame.display.update()

pygame.quit()



'''
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)

'''