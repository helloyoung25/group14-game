# 버그: 피사체가 사라졌지만 총알은 계속 맞는 버그
# 버그: 피사체가 있는 위치에 총을 쏠 경우 총알의 발사속도가 빨라짐
# 버그: 발사체의 y축 위치에 따라서 총알의 발사속도가 달라짐
# 버그: 발사체가 화면 밖으로 계속 나갈 수 있음.

# pygame 라이브러리를 가져와라.
# from multiprocessing.context import ForkServerProcess
import pygame
# pygame 라이브러리를 pg 라는 이름으로 가져와라.
import pygame as pg
from pygame.locals import *
from operator import truediv

import Actor

import random
import math
score = 0
bulletdamage = 50
FOODCOUNT = 10

bmax = 0  # bullet max
# 컬러 값을 미리 설정한다. 컴퓨터에서 컬러를 표현할때 RGB를 사용한다.
BLACK = (0, 0, 0)  # 검정
LIGHTBLUE = (0, 155, 155)
WHITE = (242, 242, 242)
YELLOW = (240, 233, 38)
ORAGNE = (255, 132, 0)

# 게임창에 텍스트를 출력하기 위한 함수코드
# printText(출력하고싶은 내용, 컬러, 위치)

# font size 추가 했습니다


def printText(msg, font_size, color=(255, 255, 255), pos=(50, 50)):
    font = pygame.font.Font('bmzua_ttf.ttf', font_size)
    textSurface = font.render(msg, True, color)
    screen.blit(textSurface, pos)


def prFirstText(msg, font_size, color=(255, 255, 255), pos=(50, 50), bgColor=(255, 132, 255)):
    font = pygame.font.Font('bmzua_ttf.ttf', font_size)
    textSurface = font.render(msg, True, color, bgColor)
    screen.blit(textSurface, pos)


def printEnergy(self):  # 체력 수치화 함수 선언
    x, y, width, height = self.getVitalStatus()

    printText(str(self.vitality)+"/"+str(self.maxVitality), 10,
              (0, 0, 0), pos=(x+(self.width/2)-15, y+height-10))

# key 입력을 기다리는 함수


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# 게임 시작화면을 구현


def show_start_screen():
    howto = pygame.image.load("howto.png")
    explain = pygame.image.load("explain.png")
    explain1 = pygame.image.load("explain1.png")
    explain2 = pygame.image.load("explain2.png")

    screen.blit(howto, (0, 0))
    pygame.display.flip()
    wait_for_key()

    screen.blit(explain, (0, 0))
    pygame.display.flip()
    wait_for_key()

    screen.blit(explain1, (0, 0))
    pygame.display.flip()
    wait_for_key()

    screen.blit(explain2, (0, 0))
    pygame.display.flip()
    wait_for_key()


# 스테이지 화면을 구현


def show_stage_screen(cnt):
    stage = pygame.image.load("stage.png")
    screen.blit(stage, (0, 0))
    printText("Stage" + str(cnt), 150, (247, 5, 5), pos=(280, nY/4))
    printText("Press Enter", 70, BLACK, pos=(58, 590))
    pygame.display.flip()
    wait_for_key()

# 게임 종료 화면


def show_ending_screen():
    end = pygame.image.load("ending_screen.jpg")
    screen.blit(end, (0, 0))
    printText("Game Over", 50, YELLOW, pos=(700, 150))
    printText("Time:"+str(elapsed_timer_hour)+":"+str(elapsed_timer_sec), 30,
              WHITE, pos=(10, 10))
    printText("Score:"+str(score), 30,  WHITE, pos=(10, 40))
    pygame.display.flip()
    wait_for_key()


# ===========================================파이게임 코딩을 시작하는 부분

# 가장 윗줄에 게임에 대한 값들을 초기화
pygame.init()


# 배경 맵
background = pygame.image.load("background.png")

# 게임 창의 X(가로)의 차원 (길이)
nX = 1010
# 게임 창의 Y(세로)의 차원 (길이)
nY = 700

bullets = []
# size라는 list 데이터로 가지고 있음
size = [nX, nY]

bulletFire = False
keyFlag = None
back_img = ["background.png", "background5.png", "background2.png",
            "background3.png", "background4.png"]  # 배경이미지 리스트
enermy_img = ["tacco.png", "cucum.png", "hambu.png",
              "melon.png", "banana.png"]  # 적이미지 리스트
attack_img = ["taccoAttack.png", "cucumAttack.png", "hambuAttack.png",
              "melonAttack.png", "bananaAttack.png"]  # 공격물체 이미지 리스트
# 게임 창의 크기를 셋팅한다.
# pygame 라이브러리 사용
screen = pygame.display.set_mode(size)
# pygame 라이브러리 사용하여 게임창의 이름을 붙여준다.
pygame.display.set_caption("escape food")

# 시간 시작 tick을 받아옴
start_ticks = pygame.time.get_ticks()

done = False
clock = pygame.time.Clock()

# Actor클래스를 사용하여 객체(주인공) 하나를 생성
hero = Actor.Actor(pygame)
hero.setImage("man.png")
hero.setScale(150, 150)
hero.setPosition(nX/2-100, nY/2 + 150)
hero.setVitality(100)
hero.estimateCenter()


# actor클래스를 사용하여 객체(적) 하나를 더 생성
enermy = Actor.Actor(pygame)
enermy.setImage("tacco.png")
enermy.setScale(180, 180)
enermy.setPosition(nX/2-100, nY/2 - 350)
enermy.setVitality(500)
enermy.estimateCenter()

# enermy 공격 물체 = 음식 (-Attack.png)
foods: list[Actor.Food] = []
for i in range(FOODCOUNT):
    food = Actor.Food(pygame)
    food.setImage("taccoAttack.png")
    food.setScale(70, 70)
    food.setPosition(nX/2, nY/2 - 350)
    food.estimateCenter()
    food.damage(10)
    foods.append(food)

# 힐팩 액터
heal = Actor.Heal(pygame)
heal.setImage("hill.png")
heal.setScale(70, 70)
heal.estimateCenter()

# 파워업 액터
PowerUp = Actor.PowerUp(pygame)
PowerUp.setImage("power.png")
PowerUp.setScale(50, 50)
PowerUp.estimateCenter()


# 총알 좌표들 모아두는 리스트

# bullet delta 총알이 날아가는 변화량
bd = -20
dx = 0
dy = 0
ds = 0

heal_flag = True

# 적이 죽은 횟수
cnt = 0


# 시작 전 화면을 보여줌
show_start_screen()
show_stage_screen(cnt+1)
# 스테이지 사이사이의 비어있는 시간을 계산
empty_ticks = pygame.time.get_ticks()-start_ticks
# 배경음악을 셋팅
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
# 반복자 while문
# done이 False를 유지하는 동안 계속 실행, not False = True
while not done:
    # set on 10 frames per second (FPS)
    clock.tick(30)

    # 게임을 실행하는 기능들을 실제로 여기에 구현

    # 스크린의 배경색을 채워넣기
    screen.fill(BLACK)
    screen.blit(background, (0, 0))

    enermysel = cnt % 5
    # 경과시간(ms)을 1000으로 나누어 초 단위로 표시s
    elapsed_timer = (pygame.time.get_ticks()-start_ticks-empty_ticks)/1000
    # 초를 분:초로 나타내기 위함
    elapsed_timer_hour = int(elapsed_timer/60)
    # 초를 분:초로 나타내기 위함
    elapsed_timer_sec = int(elapsed_timer % 60)
    # 텍스트 함수
    printText("time:"+str(elapsed_timer_hour)+":"+str(elapsed_timer_sec), 30,
              BLACK, pos=(10, 10))

    # score 표시함수
    printText("score:"+str(score), 30,  BLACK, pos=(10, 40))

    # stage 표시함수
    printText("stage:"+str(cnt+1), 30, BLACK, pos=(10, 70))

    # heal 표시
    heal_img = Actor.Heal(pygame)
    heal_img.setImage("hill.png")
    heal_img.setScale(50, 50)

    screen.blit(heal_img.actor, (10, 100))
    printText("+"+str(heal.heal_cnt), 20, BLACK, pos=(55, 120))

    # heal 표시
    power_img = Actor.Heal(pygame)
    power_img.setImage("power.png")
    power_img.setScale(50, 50)

    screen.blit(power_img.actor, (10, 150))
    printText("+"+str(PowerUp.power_cnt), 20,
              BLACK, pos=(55, 170))

    time = (pygame.time.get_ticks() - start_ticks) / 1000

    background = pygame.image.load(back_img[enermysel])  # 스테이지에 따른 배경 변화

    enermy.setImage(enermy_img[enermysel])  # 스테이지에 따른 적 이미지 변화
    enermy.setScale(180, 180)

    food.setImage(attack_img[enermysel])  # 스테이지에 따른 공격물체 변화
    food.setScale(70, 70)

    for i in range(FOODCOUNT):
        if foods[i].islive == False:
            foods[i].reset(screen)

        # 화면 밖으로 넘어가면 디진다
        if foods[i].y > screen.get_width():
            foods[i].islive = False

        # 살아있는 경우
        if foods[i].islive:
            foods[i].setImage(attack_img[enermysel])
            foods[i].setScale(70, 70)
            foods[i].drop()
            foods[i].drawActor(screen)
            foods[i].estimateCenter()
            if foods[i].isCollide(hero):
                food_time = pygame.time.get_ticks()
                foods[i].islive = False
                hero.decreaseVitality(10)
                now = pygame.time.get_ticks()
                if (now - food_time) / 1000 % 60 < 2:
                    printText("-"+str(10), 20,
                              WHITE, pos=(hero.x + hero.width/2, hero.y - 50))
                    now = pygame.time.get_ticks()

    if time % heal.interval < 0.1 and heal.islive == False:
        heal.reset(screen)

    # 힐팩이 너무 밑으로 내려가면
    if heal.y > screen.get_width():
        heal.islive = False

    if heal.islive:
        heal.drop()
        heal.drawActor(screen)
        heal.estimateCenter()
        # 히어로가 먹은 경우
        if heal.isCollide(hero):
            heal.islive = False
            # 생명력 증가량
            hero.increaseVitality(10)
            heal.heal_cnt += 1

    if time % PowerUp.interval < 0.1 and PowerUp.islive == False:
        PowerUp.reset(screen)

    # 힐팩이 너무 밑으로 내려가면
    if PowerUp.y > screen.get_width():
        PowerUp.islive = False

    if PowerUp.islive:
        PowerUp.drop()
        PowerUp.drawActor(screen)
        PowerUp.estimateCenter()
        # 히어로가 먹은 경우
        if PowerUp.isCollide(hero):
            PowerUp.islive = False
            # 공격력 증가량
            bulletdamage += 5
            PowerUp.power_cnt += 1

    # 어떤 이벤트가 들어왔을때 그 이벤트를 가져옴
    for event in pygame.event.get():

        # 그 특정 이벤트가 무엇인지 직접 확인하는 절차
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = - 18
            elif event.key == pygame.K_RIGHT:
                dx = 18
            elif event.key == pygame.K_DOWN:
                dy = 18
            elif event.key == pygame.K_UP:
                dy = -18
            elif event.key == pygame.K_SPACE:
                print("스페이스 버튼 누름")
                bulletFire = True
            elif event.key == pygame.K_x:
                pygame.quit()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                dx = 0
            elif event.key == pygame.K_RIGHT:
                dx = 0
            elif event.key == pygame.K_DOWN:
                dy = 0
            elif event.key == pygame.K_UP:
                dy = 0
    hero.estimateCenter()
    enermy.estimateCenter()
    food.estimateCenter()

    if bulletFire == True and (bmax % 4 == 0):
        bullet = Actor.Actor(pygame)
        bullet.setImage("bullet.png")
        bullet.setScale(20, 20)
        hero.estimateCenter()
        bullet.setPosition(hero.centerX, hero.centerY)
        bullet.setSound("laser.wav")
        bullet.soundPlay()
        bullets.append(bullet)

    d_bul = []
    for i in range(len(bullets)):
        bul_n = bullets[i]
        bul_n.move(0, bd)
        bul_n.drawActor(screen)
        if bul_n.y < 0:
            d_bul.append(i)
    for d in d_bul:
        del bullets[d]
    ds_bul = []  # deletescreen_bullet
    for i in range(len(bullets)):
        bul_n = bullets[i]
        bul_n.estimateCenter()
        enermy.estimateCenter()
        if bul_n.isCollide(enermy) == True:
            ds_bul.append(i)
            enermy.decreaseVitality(bulletdamage)
            score += bulletdamage
    for d in ds_bul:
        del bullets[d]

    hero.move(dx, dy)
    hero.drawActor(screen)
    hero.drawEnergyBar(screen)

    if hero.isCollide(enermy):
        print("적과 충돌함")
        hero.decreaseVitality(5)

    if hero.x < 0:
        hero.x = 0

    if hero.x > nX-150:
        hero.x = nX-150

    if hero.y < 0:
        hero.y = 0

    if hero.y > nY-150:
        hero.y = nY-150

    if enermy.x < 0:
        enermy.x = 0

    if enermy.x > nX-180:
        enermy.x = nX-180

    if enermy.y < 0:
        enermy.y = 0

    if enermy.y > nY-180:
        enermy.y = nY-180

    if enermy.isDead == False:
        enermy.drawActor(screen)
        enermy.drawEnergyBar(screen)
        printEnergy(enermy)  # 적 체력 수치화
        enermy.moveRandomly(nX, nY)

        if hero.isDead == True:
            pygame.mixer.music.stop()
            show_ending_screen()
            pygame.quit()

    elif enermy.isDead == True:
        start_empty = pygame.time.get_ticks()  # stage가 전환되는 시점 기록
        cnt += 1
        show_stage_screen(cnt+1)
        end_empty = pygame.time.get_ticks()  # 다음 stage가 시작되기 직전 시점 기록
        enermy.setVitality(500 + 300*(cnt))
        empty_ticks += (end_empty - start_empty)
        hero.setPosition(nX/2-100, nY/2 + 150)
        hero.move(0, 0)
        enermy.setPosition(nX/2-100, nY/2 - 350)
        bulletFire = False

        enermy.isDead = False

    bmax += 1
    pygame.display.update()

# 게임을 끝내는 명령어
pygame.quit()
