import pygame
import random
from time import sleep

WHITE=(255,255,255)
RED=(255,0,0)
width=1024
height=512
background_width=1024
bad_width=110
bad_height=67
aircraft_width=90
aircraft_height=55
fireball1_width=140
fireball1_height=60
fireball2_width=86
fireball2_height=60

def drawScore(count):
    global gamepad
    font=pygame.font.SysFont(None,25)
    text=font.render('Teeth fairy passed:'+str(count),True,WHITE)
    gamepad.blit(text,(0,0))

def gameOver():
    global gamepad
    dispMessage('GAME OVER')
    
def textObj(text,font): # 게임화면에 표시될 텍스트 모양과 영역 설정
    textSurface=font.render(text,True, RED)
    return textSurface, textSurface.get_rect()

def dispMessage(text):
    global gamepad
    
    largeText=pygame.font.Font('freesansbold.ttf',115)
    TextSurf,TextRect=textObj(text, largeText)
    TextRect.center=((width/2),(height/2))
    gamepad.blit(TextSurf,TextRect)
    pygame.display.update()
    sleep(2) # 2초 쉬고 게임 다시 시작
    runGame()
    # 게임 화면 정중앙에 인자로 입력된 'text'를 지정된 폰트와 폰트크기 115, 빨간색으로 출력
    
def crash():
    global gamepad, explosion_sound
    #pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosion_sound)
    dispMessage('Baam!!')
    
def drawObject(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))

def runGame():
    global gamepad, aircraft, clock, background1, background2
    global bad, fires, bullet, boom, shot_sound
    
    isShotBad=False # 총알이 bad를 명중했는지 안했는지 판단 플래그
    boom_count=0 # 맞았을때 화면 표시시간 
    bad_passed=0

    bullet_xy=[] # Lctrl 누를시 총알의 좌표 추가하는 리스트 자료
    x=width*0.05 
    y=height*0.8 # 바트 최초 좌표
    y_change=0
    
    background1_x=0 # 배경 좌상단 모서리의 x좌표=0
    background2_x=background_width
    bad_x=width
    bad_y=random.randrange(0,height)
    fire_x=width
    fire_y=random.randrange(0,height)
    random.shuffle(fires)
    fire=fires[0]
    
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # =마우스로 창닫기
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -7
                elif event.key == pygame.K_DOWN:
                    y_change = 7
                elif event.key == pygame.K_LCTRL:
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x=x+aircraft_width
                    bullet_y=y+aircraft_height/2
                    bullet_xy.append([bullet_x,bullet_y])
                #elif event.key == pygame.K_SPACE:
                #    sleep(5)
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
    
        # Clear gamepad
        gamepad.fill(WHITE)
        
        # Draw Background
        background1_x-=2
        background2_x-=2
        
        if background1_x == -background_width:
            background1_x = background_width
        if background2_x == -background_width:
            background2_x = background_width
        
        drawObject(background1,background1_x,0)
        drawObject(background2,background2_x,0)
        drawScore(bad_passed)
        
        # Check the number of Bad passed
        if bad_passed > 2:
            gameOver()
            
        # Aircraft Position
        y+=y_change
        if y<0:
            y=0
        elif y > height - aircraft_height:
            y = height - aircraft_height # 나의 y좌표를 게임판 내로 제한
        
        # Bad Position
        bad_x-=7 # bad를 캐릭터 쪽으로 7픽셀씩 날아오게 설정
        if bad_x<=0: # 왼쪽 끝까지 가면 bad 위치 재설정
            bad_passed+=1
            bad_x=width
            bad_y=random.randrange(0,height) 
        
        # Fireball Position
        if fire == None: #  fire=None일때 30픽셀씩 다가오게 함
            fire_x-=30 # 이는 방해물이 없으므로 일종의 시간 지연책
        else:
            fire_x-=15 # 불덩이라면 15픽셀씩
        
        if fire_x<=0:
            fire_x=width
            fire_y=random.randrange(0,height) # 불덩이 날아올 위치
            random.shuffle(fires)
            fire=fires[0] # 무작위 섞은 후 첫번째 요소 택, 불덩이 or None
            
        # Bullets Position
        if len(bullet_xy)!=0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0]+=15 # bullet 속도 15픽셀
                bullet_xy[i][0]=bxy[0]
                
                # Check if bullet strike Bad
                if bxy[0]>bad_x: # 발사된 bad가 명중했는지 체크 
                    if bxy[1]>bad_y and bxy[1]<bad_y+bad_height:
                        bullet_xy.remove(bxy) # 명중확인 후 제거
                        isShotBad=True
                        
                if bxy[0]>=width:# bullet이 게이판을 지나가면 bullet_xy 리스트에서 해당 좌표 삭제
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass
                
        # Check aircraft crashed by BAD, 나와 bad가 충돌했는지 체크하는 루틴
        if x+aircraft_width>bad_x:
            if (y>bad_y and y<bad_y+bad_height) or \
            (y>aircraft_height>bad_y and aircraft_height<bad_y+bad_height):
                crash()
            
        # Check aircraft crashed by Fireball, 나와 fires가 충돌했는지 체크하는 루틴
        if fire[1] != None:
            if fire[0]==0: # 체크하려는 fire의 식별자가 0이면, 
                fireball_width=fireball1_width # 첫번째 fire 이미지 정보를,
                fireball_height=fireball1_height
            elif fire[0]==1: # 식별자가 1이면,
                fireball_width=fireball2_width # 두번째 fire 이미지 정보를 취함
                fireball_height=fireball2_height
            if x+aircraft_width>fire_x: # 나와 fire가 충동하는 조건인지 체크, 충돌한 경우라면 crash()를 호출
                if (y>fire_y and y<fire_y +fireball_height) or \
                (y+aircraft_height>fire_y and y+aircraft_height<fire_y+fireball_height):
                    crash()
        drawObject(aircraft,x,y)
        
        if len(bullet_xy) !=0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)
        if not isShotBad: # bad가 명중되지 않았으면,
            drawObject(bad,bad_x,bad_y) # 화면에 유지
        else: # bad가 명중했으면,
            drawObject(boom,bad_x,bad_y) #bad위치에 boom 이미지 그림
            boom_count+=1
            if boom_count>5: # while문 5번 돌때까지 화면에 표시
                boom_count=0
                bad_x=width
                bad_y=random.randrange(0,height-bad_height)
                isShotBad=False
       
        if fire[1] != None:
            drawObject(fire[1],fire_x,fire_y)

        pygame.display.update()
        clock.tick(60) # FPS=60
    pygame.quit()    
    quit()

def initGame():
    global gamepad, aircraft, clock, background1, background2
    global bad, fires, bullet, boom
    global shot_sound, explosion_sound
    fires=[] # 불덩이 2개와 객체 5개 담을 리스트

    pygame.init()
    gamepad=pygame.display.set_mode((width,height))  # pad = 1024 x 512
    pygame.display.set_caption('ToothFairyFly') # title 
    aircraft=pygame.image.load('/Workspace/SimpleGame/ToothFairyShooting/tee.png')
    background1=pygame.image.load('/Workspace/SimpleGame/ToothFairyShooting/tree_bg.png')
    background2=background1.copy()
    bad=pygame.image.load('/Workspace/SimpleGame/ToothFairyShooting/bad.png')
    fires.append((0,pygame.image.load('/Workspace/SimpleGame/ToothFairyShooting/fire1.png')))
    fires.append((1,pygame.image.load('/Workspace/SimpleGame/ToothFairyShooting/fire2.png')))
    # fires의 이미지 크기가 다르므로 어떤것이 나와 충돌했는지 체크하기 위한 식별자 
    boom=pygame.image.load('/Workspace/SimpleGame/ToothFairyShooting/teeth.png')
    shot_sound=pygame.mixer.Sound('/Workspace/SimpleGame/ToothFairyShooting/shot.wav')
    explosion_sound=pygame.mixer.Sound('/Workspace/SimpleGame/ToothFairyShooting/explosion.wav')
    #pygame.mixer.music.load('.wav')
    #pygame.mixer.music.play(-1)
    
    for i in range(5):
        fires.append((i+2,None))
        
    bullet=pygame.image.load('/Workspace/SimpleGame/ToothFairyShooting/teeb.png')
    clock=pygame.time.Clock() # 초당 프레임(FPS)
    runGame()

if __name__=='__main__':
    initGame()

