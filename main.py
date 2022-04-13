import pygame
import sys
import random

# Inicialização
pygame.init()
clock = pygame.time.Clock()

# Configurando a janela
screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')

# Objetos
ball = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
player = pygame.Rect(screenWidth - 20, screenHeight / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight / 2 - 70, 10, 140)

# Variáveis
ballSppedX = 0.5
ballSppedY = 0.5
opponentSpeed = 10


def inputs():
    # Processando as entradas (eventos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Controlar com as setas e W,S
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         if player.y > 40:
        #             player.y -= 40
        #     if event.key == pygame.K_DOWN:
        #         if player.y < 960 - 180:
        #             player.y += 40
        #
        #     if event.key == pygame.K_w:
        #         if opponent.y > 40:
        #             opponent.y -= 40
        #     if event.key == pygame.K_s:
        #         if opponent.y < 960 - 180:
        #             opponent.y += 40

    # Controlar player com o Mouse
    (x, y) = pygame.mouse.get_pos()
    if 820 > y > 0:
        player.y = y

    # Movimento do inimigo
    if opponent.bottom < ball.y:
        opponent.bottom += opponentSpeed
    if opponent.top > ball.y:
        opponent.top -= opponentSpeed


def draw():
    # Desenho
    screen.fill((0, 0, 0))
    pygame.draw.ellipse(screen, (200, 200, 200), ball)
    pygame.draw.rect(screen, (200, 200, 200), player)
    pygame.draw.rect(screen, (200, 200, 200), opponent)


def update():
    global ballSppedX, ballSppedY

    # Atualizacao
    dt = clock.tick(60)
    ball.x += ballSppedX * dt
    ball.y += ballSppedY * dt
    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballSppedY *= -1

    if ball.bottom >= opponent.top and ball.top <= opponent.bottom and ball.left <= opponent.right:
        # Efeito na batida
        delta = ball.centery - opponent.centery
        ballSppedY = delta * 0.01
        ballSppedX *= -1

    if ball.bottom >= player.top and ball.top <= player.bottom and ball.right >= player.left:
        # Efeito na batida
        delta = ball.centery - player.centery
        ballSppedY = delta * 0.01
        ballSppedX *= -1

    # Atualizando a janela 60fps
    pygame.display.flip()


def resetBall():
    global ballSppedX, ballSppedY
    if ball.x > 1310 or ball.x < -30:
        ball.center = (screenWidth/2, screenHeight/2)
        ballSppedX *= random.choice((-1,1))


# Game Loop
while True:
    inputs()
    draw()
    resetBall()
    update()
