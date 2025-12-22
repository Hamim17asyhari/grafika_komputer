# APLIKASI GRAFIKA 2D - LOGO BABI GEOMETRIS
# Algoritma: DDA, Midpoint Circle, Poligon, Transformasi 2D
# TANPA FUNCTION

import pygame
import math

pygame.init()

# =========================
# WINDOW
# =========================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Logo Babi Geometris")
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

screen.fill(WHITE)

# =========================
# TRANSFORMASI
# =========================
tx, ty = 0, -10          # Translasi mata
scale = 1.2              # Skala hidung

# ==================================================
# 1. MIDPOINT CIRCLE - WAJAH
# ==================================================
xc, yc = 400, 320
r = 150
x = 0
y = r
p = 1 - r

while x <= y:
    screen.set_at((xc+x, yc+y), BLACK)
    screen.set_at((xc-x, yc+y), BLACK)
    screen.set_at((xc+x, yc-y), BLACK)
    screen.set_at((xc-x, yc-y), BLACK)
    screen.set_at((xc+y, yc+x), BLACK)
    screen.set_at((xc-y, yc+x), BLACK)
    screen.set_at((xc+y, yc-x), BLACK)
    screen.set_at((xc-y, yc-x), BLACK)

    if p < 0:
        p = p + 2*x + 3
    else:
        p = p + 2*(x-y) + 5
        y -= 1
    x += 1

# ==================================================
# 2. MIDPOINT CIRCLE - HIDUNG (SKALA)
# ==================================================
xc, yc = 400, 360
r = int(50 * scale)
x = 0
y = r
p = 1 - r

while x <= y:
    screen.set_at((xc+x, yc+y), BLACK)
    screen.set_at((xc-x, yc+y), BLACK)
    screen.set_at((xc+x, yc-y), BLACK)
    screen.set_at((xc-x, yc-y), BLACK)
    screen.set_at((xc+y, yc+x), BLACK)
    screen.set_at((xc-y, yc+x), BLACK)
    screen.set_at((xc+y, yc-x), BLACK)
    screen.set_at((xc-y, yc-x), BLACK)

    if p < 0:
        p = p + 2*x + 3
    else:
        p = p + 2*(x-y) + 5
        y -= 1
    x += 1

# Lubang hidung
for i in range(-5,6):
    for j in range(-5,6):
        screen.set_at((385+i, 360+j), BLACK)
        screen.set_at((415+i, 360+j), BLACK)

# ==================================================
# 3. MIDPOINT CIRCLE - MATA (TRANSLASI)
# ==================================================
for ex in [360, 440]:
    xc, yc = ex + tx, 300 + ty
    r = 15
    x = 0
    y = r
    p = 1 - r
    while x <= y:
        screen.set_at((xc+x, yc+y), BLACK)
        screen.set_at((xc-x, yc+y), BLACK)
        screen.set_at((xc+x, yc-y), BLACK)
        screen.set_at((xc-x, yc-y), BLACK)
        screen.set_at((xc+y, yc+x), BLACK)
        screen.set_at((xc-y, yc+x), BLACK)
        screen.set_at((xc+y, yc-x), BLACK)
        screen.set_at((xc-y, yc-x), BLACK)
        if p < 0:
            p = p + 2*x + 3
        else:
            p = p + 2*(x-y) + 5
            y -= 1
        x += 1

# ==================================================
# 4. GARIS DDA - ALIS MARAH
# ==================================================
# KIRI
x1,y1 = 330,260
x2,y2 = 380,280
dx = x2-x1
dy = y2-y1
steps = max(abs(dx),abs(dy))
x_inc = dx/steps
y_inc = dy/steps
x,y = x1,y1
for i in range(int(steps)):
    screen.set_at((int(x),int(y)),BLACK)
    x += x_inc
    y += y_inc

# KANAN
x1,y1 = 470,260
x2,y2 = 420,280
dx = x2-x1
dy = y2-y1
steps = max(abs(dx),abs(dy))
x_inc = dx/steps
y_inc = dy/steps
x,y = x1,y1
for i in range(int(steps)):
    screen.set_at((int(x),int(y)),BLACK)
    x += x_inc
    y += y_inc

# ==================================================
# 5. POLIGON - TELINGA
# ==================================================
# TELINGA KIRI
points = [(280,150),(330,70),(360,170)]
for i in range(len(points)):
    x1,y1 = points[i]
    x2,y2 = points[(i+1)%len(points)]
    dx = x2-x1
    dy = y2-y1
    steps = max(abs(dx),abs(dy))
    x_inc = dx/steps
    y_inc = dy/steps
    x,y = x1,y1
    for j in range(int(steps)):
        screen.set_at((int(x),int(y)),BLACK)
        x += x_inc
        y += y_inc

# TELINGA KANAN (REFLEKSI)
for i in range(len(points)):
    x1,y1 = points[i]
    x2,y2 = points[(i+1)%len(points)]
    x1 = WIDTH - x1
    x2 = WIDTH - x2
    dx = x2-x1
    dy = y2-y1
    steps = max(abs(dx),abs(dy))
    x_inc = dx/steps
    y_inc = dy/steps
    x,y = x1,y1
    for j in range(int(steps)):
        screen.set_at((int(x),int(y)),BLACK)
        x += x_inc
        y += y_inc

# =========================
# TEKS JUDUL
# =========================
font = pygame.font.SysFont("arial", 48, True)
text = font.render("BABI RACING", True, BLACK)
text_rect = text.get_rect(center=(400, 520))
screen.blit(text, text_rect)

pygame.display.update()

# =========================
# LOOP
# =========================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)

pygame.quit()
