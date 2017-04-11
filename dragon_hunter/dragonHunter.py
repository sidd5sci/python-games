import pygame
import time,math,random

# initalize the game
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()
width,height = 640,480
screen = pygame.display.set_mode((width,height),0,32)

#  global variables

gameOver = False
time = 0.0
# score 
gameScore = 0.0
# player 
playerSpeedX = 0.0
playerSpeedY = 0.0
playerPosX = 500.0
playerPosY = 400.0
playerHealth = 100
#  enemy 
enemyPosX,enemyPosY = 0.0,400.0
enemySpeedX,enemySpeedY = 1.0,-10.0
enemyDisplay = False
enemyHealth = 100
dragonFire = False
timer = 0 # fire up time
# bullet 
gameBullets = 100
bulletRelode = False
bulletFire = False
bullet = False
bulletPosX,bulletPosY = -10.0,-10.0
bulletSpeedX,bulletSpeedY = 0.0,0.0
bulletCount = 6



def drawEnvironment():
    # draw grass
    grass = pygame.image.load("resources/images/back.png")
    screen.blit(grass,(0,0))
    
def playSounds():
    fileName = 'resources/sound/gun-shot.wav'
    bulletSound = pygame.mixer.Sound(fileName)
    pygame.mixer.Sound.play(bulletSound)
    
def gameLogic():
    global height,width,bulletCount,timer,dragonFire,playerHealth,gameOver,enemySpeedY,enemySpeedX,enemyPosX,enemyHealth,enemyPosY,enemyDisplay,playerSpeedX,playerSpeedY ,playerPosX,playerPosY,bulletRelode,gameBullets  
    font = pygame.font.SysFont("calibri",40)
    # player motion
    playerPosX += playerSpeedX
    playerPosY += playerSpeedY
    if gameBullets <= 0:
        bulletRelode = Ture
    
    if playerPosY+65 >480:
        playerPosY = 420
    
    if playerPosY-65 <280:
       playerPosY = 360
    # dragon fire display    
    dragonFireDisplay()
    # enemy appear when player is close
    if playerPosX <= 200:
        enemyDisplay = True
    
        
    
    
       
    # enemy wlking 
    if enemyPosX <= 0.0:
          enemySpeedX = +1.0
    if enemyPosX >= 70.0:
          enemySpeedX = -1.0
    enemyPosX += enemySpeedX

    if enemyPosY <= 320.0:
          enemySpeedY = +10.0
    if enemyPosY >= 500.0:
          enemySpeedY = -10.0
    enemyPosY += enemySpeedY
    # dragon fire logic 
    if playerPosX <= 200 and (random.uniform(0,100) < 10):
        dragonFire = True
        timer = 10
    elif playerPosX >200:
        dragonFire = False
    elif timer <= 0:
        dragonFire = False
        
    timer -= 1
    
    # enemy helath logic
    slope = 0.0
      #pygame.draw.line(screen,(254,0,0),[enemyPosX,enemyPosY],[playerPosX,playerPosY],1)
    slope = (playerPosY-enemyPosY)/(playerPosX-enemyPosX)
    slope = (slope*180)/math.pi
      # enemy health decrease
    textWin = font.render("You Win",True,(254,254,254))
    if slope < 0.0 and slope >-3.0 or slope >0.0 and slope < 15.0:
        if bulletFire == True and playerPosX <200:

            if enemyHealth <= 0 :
                gameOver = True
                enemyDisplay = False
                screen.blit(textWin,[width/2-50,height/2])
            else:
                 enemyHealth -= 5
    # enemy health display             
    pygame.draw.rect(screen,(254,0,0),[10,10,enemyHealth*2,15],3)
    pygame.draw.rect(screen,(254,0,0),[10,10,100*2,15],1)
    # player health display             
    pygame.draw.rect(screen,(50,100,200),[410,10,playerHealth*2,15],3)
    pygame.draw.rect(screen,(50,100,200),[410,10,100*2,15],1)
    # player health logic
    dist = 0.0 
    dist =(playerPosX-enemyPosX) +70
    textLoose = font.render("You Loose!",True,(254,54,54))
    if dist <= 200 and dragonFire == True:
        playerHealth -=1
    if dist <= 150 and dragonFire == True:
        playerHealth -= 3
    if dist <100 and dragonFire == True:
        playerHealth -= 5
    if dist <50 and dragonFire == True:
        playerHealth -=10
    if playerHealth <= 0:
        gameOver =True
        screen.blit(textLoose,[width/2-70,height/2])
    # bullets reload logic
   
    textReload = font.render("Reload press r",True,(254,54,54))
    
    if bulletCount <= 0:
        bulletReload = True
        screen.blit(textReload,[width/2-100,height/2])
    else:
        fireBullet()
    
    
def drawPlayer():
    global playerPosX,playerPosY
    player = pygame.image.load("resources/images/player3.png")
    screen.blit(player,(playerPosX,playerPosY))
    
def enemy():
    global time,enemyPosX,enemyPosY,enemyDisplay
    enemy = pygame.image.load("resources/images/player.png")
    enemyDead = pygame.image.load("resources/images/player1.png")
    if enemyDisplay == True:
        screen.blit(enemy,(enemyPosX,enemyPosY))
    if gameOver == True and enemyDisplay == False:
        screen.blit(enemyDead,(enemyPosX,enemyPosY))
def input_():
    global bulletFire,bulletCount,playerSpeedX,playerSpeedY,bullet
    # loop through the events
    for event in pygame.event.get():
        #check if the event is the x button
        if event.type==pygame.QUIT:
            #if it is quit the game
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bulletFire = True
            buttet = True
            bulletCount -= 1
        elif event.type == pygame.MOUSEBUTTONUP:
            bulletFire = False   
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerSpeedX = -8.0
            if event.key == pygame.K_RIGHT:
                playerSpeedX = +8.0
            if event.key == pygame.K_UP:
                playerSpeedY = -10.0
            if event.key == pygame.K_DOWN:
                playerSpeedY = +10.0
            if event.key == pygame.K_RCTRL:
                bulletCount = 6
            if event.key == pygame.K_r:
                bulletCount = 6
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerSpeedX = 0.0
            if event.key == pygame.K_RIGHT:
                playerSpeedX = 0.0
            if event.key == pygame.K_UP:
                playerSpeedY = 0.0
            if event.key == pygame.K_DOWN:
                playerSpeedY = 0.0


def fireBullet():
    global playerPosX,playerPosY,bulletFire,bullet
    bullet_ = pygame.image.load("resources/images/bullet.png")
    fire = pygame.image.load("resources/images/fire.png")
    bulletPosX = playerPosX -25
    bulletPosY = playerPosY+20
    if bulletFire == True:
        screen.blit(fire,(playerPosX-20,playerPosY+5))
        screen.blit(bullet_,(bulletPosX,bulletPosY))
        playSounds()
    if bullet == True:
        screen.blit(bullet_,(bulletPosX,bulletPosY))
def dragonFireDisplay():
    global enemyPosX,enemyPosY,dragonFire
    fire = pygame.image.load("resources/images/fire2.png")
    file1= 'resources/sound/dragon-roar.wav'
    if dragonFire == True:
        screen.blit(fire,(enemyPosX+70,enemyPosY+5))
        dragonFireSound = pygame.mixer.Sound(file1)
        pygame.mixer.Sound.play(dragonFireSound)
drawEnvironment()
drawPlayer()
# update the screen
pygame.display.update()
#playSounds()

#pygame.mixer.Sound("Bike_Rides.mp3")
clock = pygame.time.Clock()
# main loop

while  gameOver != True:
    
    # input section
    input_()
    # game logics
    gameLogic()
    # draw the screen element
    drawEnvironment()
    drawPlayer()
    enemy()
    gameLogic()
    # update the screen
    pygame.display.update()
    # clear the screen
    screen.fill(0)
    # frame rate
    clock.tick(60)
    time += 0.015
    if gameOver == True :
        input_()

        
