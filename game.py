import pygame, random, sys ,os,time
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
#color('red','green','blue')
TEXTCOLOR = (255,255,255)  #staring game title words (255,255,0) is yellow 
BACKGROUNDCOLOR = (0, 0, 0) #black->(0, 0, 0) ,white->(255,255,255) 
FPS = 30
BADDIEMINSIZE = 30  #baddie min size  ??
BADDIEMAXSIZE = 40  #baddie max size  ??
BADDIEMINSPEED = 8  #baddie min speed
BADDIEMAXSPEED = 20  #baddie max speed (baddie反派角色)
ADDNEWBADDIERATE = 6 #addnewbaddierate
PLAYERMOVERATE = 8   #moving rate
count=3

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):  
    #(playerRect是玩家在畫面上的位置與矩形的大小)
    #baddies is a dict ，字典中有一個鍵 'rect'，代表敵人的矩形。這個矩形用來表示敵人在遊戲畫面上的位置和大小
    #簡單來說，b['rect'] 是取得特定敵人所對應的矩形 
    for b in baddies: 
        if playerRect.colliderect(b['rect']):  #playerRect.colliderect 碰撞測試
            return True
    return False

def drawText(text, font, surface, x, y):
     #font.render #使用指定的字型 font 將文字 text 轉換為文字表面（text surface）
     #font.render #(文字內容,字型(created using python.font.Font()),文字)
    textobj = font.render(text, 1, TEXTCOLOR)  #(文字內容,1,文字顏色)
    textrect = textobj.get_rect()  #取得文字表面的矩形，這個矩陣用於處理文字的位置與對齊方式
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)#將文字textobj繪製到surface上,位置

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#視窗大小
pygame.display.set_caption("car racing")#視窗名稱
pygame.mouse.set_visible(True)  #滑鼠是否顯示


#pygame.init()
#pygame.time.Clock()
#pygame.display.set_mode((width,height))
#pygame.display.set_caption("the title of game")
#pygame.mouse.set_visible()



# fonts(字型,字體)
font = pygame.font.SysFont(None, 30)#(Press any key to start the game) ,一開始的提示字元大小
# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/d1.wav')  #below has pygame.mixer.music.load
laugh = pygame.mixer.Sound('music/dinter.wav')


# images
playerImage = pygame.image.load('image/car1.png') #操控的車
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car4.png')
playerRect = playerImage.get_rect()  #image.get_rect()取得圖片的矩形，大小
baddieImage = pygame.image.load('image/car2.png')
sample = [car3,car4,baddieImage]
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')


# "Start" screen
drawText('Press any key to start the game!', font, windowSurface, (WINDOWWIDTH/3.5), (WINDOWHEIGHT /2.5))
drawText('And Enjoy!', font, windowSurface, (WINDOWWIDTH / 3)+60, (WINDOWHEIGHT / 2.5)+30)
#drawText(text,font,surface,x,y) is function (文字,大小&字形,介面,x,y)
#drawText is function , show text on display  
pygame.display.update()
waitForPlayerToPressKey()
zero=0
if not os.path.exists("data/save.dat"):
    f=open("data/save.dat",'w')
    f.write(str(zero))
    f.close()   #   
v=open("data/save.dat",'r')
topScore = int(v.readline())
v.close()
while (count>0):
    # start of the game
    baddies = []   
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 3, WINDOWHEIGHT - 50)#車起始位置
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1,0.0) #(number of repeat,start point ,end point)  -1 ->(loop repeat)

    while True: # the game loop
        score += 1 # increase score

        for event in pygame.event.get():
            
            if event.type == QUIT:
                terminate()
            # 返回 慢動作 上 下 左 右
            if event.type == KEYDOWN:
                if event.key == ord('z'):  #ord is represents the z unicode 
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_UP or event.key == ord('w'): #K_UP full name pygame.locals.K_UP
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                if event.key == K_LEFT or event.key == ord('a'):  #K_LEFT is left button
                    moveRight = False                     #K_LEFT is a constant represents left arrow key
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
        


            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:   # esc button
                        terminate()
            

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
        # for event in pygame.event.get(): end

        # Add new baddies at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:  #add_new_baddie_rate
            baddieAddCounter = 0    
            baddieSize =30
            '''1.rect 
               newBaddie={ 'rect',random.randint(隨機變數介於140-485間),敵人出現的水平位置}
                            ,0-baddieSize 是垂直出現的位置,baddieSize是一個參數 
                            ,23 敵人的寬 並不是圖片的高度 圖片外觀的大小不變 車子還沒碰到圖片,就會判斷為撞到
                            ,47 敵人的高 並不是圖片的高度
                2.speed 
               newBaddie={
                          random.randint(最小速度,最大速度)
               }
                3.surface pygame.transform.scale random.choice(sample)選擇sample中的圖片OR外觀
                        

      
            '''
                       
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(sample), (23, 47)),
                        }
            baddies.append(newBaddie)   #baddies=[]
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (126, 599)),
                       }
            baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(497,0,303,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (303, 599)),
                       }
            baddies.append(sideRight)
            print("baddies=\n",baddies)
            

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface,128, 40)
        
        windowSurface.blit(playerImage, playerRect)

        
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                g=open("data/save.dat",'w')
                g.write(str(score))
                g.close()
                topScore = score
            break

        mainClock.tick(FPS)

    # "Game Over" screen.
    pygame.mixer.music.stop()
    count=count-1
    gameOverSound.play()
    time.sleep(1)
    if (count==0):
     laugh.play()
     drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
     drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
     pygame.display.update()
     time.sleep(2)
     waitForPlayerToPressKey()
     count=3
     gameOverSound.stop()
