import pygame
import sys
import random
import time

# Init
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Screen configs
screenWidth = 936
screenHeight = 626
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Retro Pong')
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

# Variables
ballSpeedX = 0.2
ballSpeedY = 0.2
opponentSpeed = 8
scored = True
blockX = random.randint(0, screenWidth - 50)
blockY = random.randint(0, screenHeight - 50)
onMenu = True
onCountdown = False
onGame = False
onVictory = False
onDefeat = False
previous = None
t = 5

# Objects
ball = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
player = pygame.Rect(695, screenHeight / 2 - 70, 10, 140)
opponent = pygame.Rect(85, screenHeight / 2 - 70, 10, 140)

# Points variables
playerPoints = 0
opponentPoints = 0


def inputs():
    # Processing inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controlling player with mouse
    (x, y) = pygame.mouse.get_pos()
    if 820 > y > 0:
        player.y = y

    # Moving opponent
    if opponent.bottom < ball.y:
        opponent.bottom += opponentSpeed
    if opponent.top > ball.y:
        opponent.top -= opponentSpeed


def draw():
    # Draw
    screen.fill((0, 0, 0))

    # Draw entities
    pygame.draw.ellipse(screen, (200, 200, 200), ball)
    pygame.draw.rect(screen, (200, 200, 200), player)
    pygame.draw.rect(screen, (200, 200, 200), opponent)

    # Drawing background
    background = pygame.image.load('oldTv.png')
    background = pygame.transform.scale(background, (936, 626))
    screen.blit(background, (screenWidth / 2 - background.get_width() / 2, 0))

    # Draw middle line
    dots = 65
    while dots < 560:
        pygame.draw.rect(screen, (200, 200, 200), (400, dots, 5, 5), 5)
        dots += 20


def update(dt):
    global ballSpeedX, ballSpeedY

    # Moving ball
    ball.x += ballSpeedX * dt
    ball.y += ballSpeedY * dt

    # Checking ball collision with screen limits and fixing bugs
    if ball.top < 60:
        ballSpeedY = abs(ballSpeedY)
    if ball.bottom > 560:
        ballSpeedY = -abs(ballSpeedY)

    # Checking ball collision with opponent
    if ball.bottom >= opponent.top and ball.top <= opponent.bottom and ball.left <= opponent.right:
        # Impact effect
        delta = ball.centery - opponent.centery
        ballSpeedY = delta * 0.01
        ballSpeedX = abs(ballSpeedX)

    # Checking ball collision with player
    if ball.bottom >= player.top and ball.top <= player.bottom and ball.right >= player.left:
        # Impact effect
        delta = ball.centery - player.centery
        ballSpeedY = delta * 0.01
        ballSpeedX = -abs(ballSpeedX)
    points()
    resetBall()

    # Updating screen as 60 fps
    pygame.display.flip()


def resetBall():
    global ballSpeedX, ballSpeedY, scored

    # Getting ball position
    if ball.x > 720 or ball.x < 60:
        # Resetting ball position to center
        ball.center = (400, 310)

        # Randomizing ball spawn velocity
        ballSpeedX *= random.choice((-1, 1))

        # Changing ball scale to make game harder
        ball.width -= 1
        ball.height -= 1

        scored = True


def points():
    global playerPoints, opponentPoints, scored, onVictory, onDefeat

    # Getting ball position
    if ball.x < 60 and scored == True:
        playerPoints += 1
        scored = False
    if ball.x > 720 and scored == True:
        opponentPoints += 1
        scored = False

    # Selecting Fonts
    usersFont = pygame.font.SysFont('OCR A Extended', 20)
    pointsFont = pygame.font.SysFont('OCR A Extended', 80)

    # Points Surfaces
    opponentPoints_surface = pointsFont.render(str(opponentPoints), False, (255, 255, 255))
    playerPoints_surface = pointsFont.render(str(playerPoints), False, (255, 255, 255))

    # Player Label
    player_surface = usersFont.render("PLAYER", False, (255, 255, 255))
    screen.blit(player_surface, (530, 70))

    # Opponent Label
    opponent_surface = usersFont.render("OPPONENT", False, (255, 255, 255))
    screen.blit(opponent_surface, (opponent_surface.get_width() * 2 - opponentPoints_surface.get_width() / 4, 70))

    # Drawing points text
    screen.blit(playerPoints_surface, (420, 60))
    screen.blit(opponentPoints_surface, (380 - opponentPoints_surface.get_width(), 60))

    # Choosing winner
    if playerPoints == 1:
        victory()
    if opponentPoints == 1:
        defeat()


def mainMenu():
    # Drawing background
    menu = pygame.image.load('menuImg.png')
    screen.blit(menu, (0, 0))
    pygame.display.flip()


def countDown():
    global previous, t, onCountdown, onGame

    # Countdown timer
    while t >= 0:
        pygame.display.flip()
        screen.fill((0, 0, 0))

        time.sleep(1)
        # Setting fonts
        pointsFont = pygame.font.SysFont('OCR A Extended', 200)
        TextFont = pygame.font.SysFont('OCR A Extended', 40)
        midiasFont = pygame.font.SysFont('OCR A Extended', 20)

        # Surfaces
        harder_surface = midiasFont.render("Game will become harder over time!", False, (255, 100, 100))
        screen.blit(harder_surface, (screenWidth / 2 - harder_surface.get_width() / 2, 0))

        pointsNeeded_surface = midiasFont.render("10 points to victory", False, (100, 255, 100))
        screen.blit(pointsNeeded_surface,
                    (screenWidth / 2 - pointsNeeded_surface.get_width() / 2, harder_surface.get_height()))

        countDownTimer_surface = pointsFont.render(str(t), False, (255, 255, 255))
        screen.blit(countDownTimer_surface, (screenWidth / 2 - countDownTimer_surface.get_width() / 2,
                                             screenHeight / 2 - countDownTimer_surface.get_height() / 2))
        startingText_surface = TextFont.render("Game Starting in:", False, (255, 255, 255))
        screen.blit(startingText_surface, (
            screenWidth / 2 - startingText_surface.get_width() / 2,
            screenHeight / 2 - countDownTimer_surface.get_height() / 1.5))
        followMe_surface = midiasFont.render("Follow me on:", False, (255, 255, 255))

        screen.blit(followMe_surface, (
            screenWidth / 2 - followMe_surface.get_width() / 2,
            screenHeight / 2 + countDownTimer_surface.get_height() / 2))

        # Midias Surfaces
        github_surface = midiasFont.render("Github: igorNeves007", False, (58, 254, 199))
        instagram_surface = midiasFont.render("Instagram: igor_mn123", False, (221, 42, 123))
        twitch_surface = midiasFont.render("Twitch: igaaoo", False, (145, 70, 255))

        # Showing midias by timer
        if t == 4:
            screen.blit(github_surface, (screenWidth / 2 - github_surface.get_width() / 2,
                                         screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height()))
        if t == 3:
            screen.blit(github_surface, (screenWidth / 2 - github_surface.get_width() / 2,
                                         screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height()))
            screen.blit(instagram_surface, (screenWidth / 2 - instagram_surface.get_width() / 2,
                                            screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height() + github_surface.get_height()))

        if t == 2:
            screen.blit(github_surface, (screenWidth / 2 - github_surface.get_width() / 2,
                                         screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height()))
            screen.blit(instagram_surface, (screenWidth / 2 - instagram_surface.get_width() / 2,
                                            screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height() + github_surface.get_height()))
            screen.blit(twitch_surface, (screenWidth / 2 - twitch_surface.get_width() / 2,
                                         screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height() + github_surface.get_height() + instagram_surface.get_height()))

        if t == 1:
            screen.blit(github_surface, (screenWidth / 2 - github_surface.get_width() / 2,
                                         screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height()))
            screen.blit(instagram_surface, (screenWidth / 2 - instagram_surface.get_width() / 2,
                                            screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height() + github_surface.get_height()))
            screen.blit(twitch_surface, (screenWidth / 2 - twitch_surface.get_width() / 2,
                                         screenHeight / 2 + countDownTimer_surface.get_height() / 2 + followMe_surface.get_height() + github_surface.get_height() + instagram_surface.get_height()))

        t -= 1
        print(t)

    print("Game Started!")
    onCountdown = False
    onGame = True
    previous = pygame.time.get_ticks()


def victory():
    global onGame, onVictory
    onGame = False
    onVictory = True


def defeat():
    global onGame, onDefeat
    onGame = False
    onDefeat = True


lag = 0
FPS = 30
MS_PER_UPDATE = 1000 / FPS

# Main Menu
while onMenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check Mouse Click
        if event.type == pygame.MOUSEBUTTONDOWN:
            onMenu = False
            onCountdown = True

    mainMenu()

# Countdown timer Screen
while onCountdown:
    countDown()

# Game
while onGame:
    current = pygame.time.get_ticks()
    elapsed = current - previous
    previous = current
    lag += elapsed
    draw()

    while lag >= MS_PER_UPDATE:
        update(MS_PER_UPDATE)
        lag -= MS_PER_UPDATE

    inputs()

while onVictory:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    victoryFont = pygame.font.SysFont('OCR A Extended', 150)
    infoFont = pygame.font.SysFont('OCR A Extended', 20)

    victorySurface = victoryFont.render("You win", False, (50, 255, 50))
    screen.blit(victorySurface,
                (screenWidth / 2 - victorySurface.get_width() / 2, screenHeight / 2 - victorySurface.get_height() / 2))

    infoSurface = infoFont.render("<Click to close>", False, (255, 255, 255))
    screen.blit(infoSurface,
                (screenWidth / 2 - infoSurface.get_width() / 2, screenHeight / 2 + victorySurface.get_height()))

    pygame.display.flip()

while onDefeat:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    defeatFont = pygame.font.SysFont('OCR A Extended', 150)
    infoFont = pygame.font.SysFont('OCR A Extended', 20)

    defeatSurface = defeatFont.render("You lose", False, (255, 50, 50))
    screen.blit(defeatSurface,
                (screenWidth / 2 - defeatSurface.get_width() / 2, screenHeight / 2 - defeatSurface.get_height() / 2))

    infoSurface = infoFont.render("<Click to close>", False, (255, 255, 255))
    screen.blit(infoSurface,
                (screenWidth / 2 - infoSurface.get_width() / 2, screenHeight / 2 + defeatSurface.get_height()))
    pygame.display.flip()
