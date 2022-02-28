from numpy import sqrt
from random import randint
import pygame as pg

class Ball:
    def __init__(self, screen : pg.Surface, x = 0, y = 0, color = (255,255,255), radius = 10, xinc = 0, yinc = 0, baseSpeed = 0.2):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.radius = radius
        self.xinc = xinc
        self.yinc = yinc
        self.v = sqrt(self.yinc ** 2 + self.xinc ** 2)
        self.baseSpeed = baseSpeed
        self.dead = False
    
    def updatePos(self):
        if self.x > (self.screen.get_width() - self.radius) or self.x < (0 +self.radius):
            self.xinc *= -1
        if self.y < (0 +self.radius):
            self.yinc *= -1
        if self.y > self.screen.get_height():
                #pg.time.wait(1000)
                self.xinc = 0
                self.yinc = 0
                self.v = 0
                self.dead = True
        self.x += self.xinc
        self.y += self.yinc
    
    def drawBall(self):
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
    
    def calculateSpeed(self):
        self.v = sqrt(self.yinc**2 + self.xinc**2)

class Brick(pg.Rect):
    def __init__(self, x, y, screen):
        pg.Rect.__init__(self, x, y, 100, 50)
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.status = True
        self.screen = screen

    def checkCrash(self, ball : Ball):
        if self.x < ball.x < self.x +100 and ((self.y+48 < ball.y < self.y +50) or (self.y < ball.y < self.y +2)) and self.status == True:
            ball.yinc *= -1
            self.status = False
        if self.y < ball.y < self.y +50 and ((self.x + 98 < ball.x < self.x +100) or (self.x < ball.x < self.x +2)) and self.status == True:
            ball.xinc *= -1
            self.status = False
    def drawBrick(self):
        pg.draw.rect(self.screen, self.color, self)

class Racket:
    def __init__(self, screen : pg.Surface, ball : Ball, x = 0, y = 0, v = 0.2):
        self.x = x
        self.y = y
        self.v = v
        self.image = pg.image.load(r".\resources\electric00.png")
        self.image2 = pg.image.load(r".\resources\electric01.png")
        self.image3 = pg.image.load(r".\resources\electric02.png")
        self.images = [self.image, self.image2, self.image3]
        self.screen = screen
        self.color = (255,255,255)
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.state = 0
        self.ball = ball

    def moveRacket(self, direction):
        if direction == "R" and self.x < self.screen.get_width() - self.width:
            self.x += self.v
            if self.ball.xinc == 0 and self.ball.yinc == 0:
                self.ball.x += self.v
        if direction == "L" and self.x > 0:
            self.x -= self.v
            if self.ball.xinc == 0 and self.ball.yinc == 0:
                self.ball.x -= self.v
            
    def checkBallHitsRacket(self):
        if ((self.x + self.width -5 < self.ball.x < self.x + self.width) or (self.x < self.ball.x < self.x + 5)) and (self.y < self.ball.y < self.y + self.height):
                self.ball.xinc *= -1
                if pg.key.get_pressed()[pg.K_RIGHT]:
                    self.ball.x += self.v * 2
                if pg.key.get_pressed()[pg.K_LEFT]:
                    self.ball.x -= self.v * 2
        if (self.x < self.ball.x < self.x +self.width) and ((self.y < self.ball.y < self.y + 2) or (self.y +self.height-2 < self.ball.y < self.y + self.height)):
                self.ball.yinc *= -1
                if self.ball.xinc < 0:
                    negx = -1
                else:
                    negx = 1
                if self.ball.yinc < 0:
                    negy = -1
                else:
                    negy = 1
                if self.ball.x < self.x + self.width // 2:
                    self.ball.yinc = self.ball.baseSpeed * (75 + 0.5 * (self.ball.x-self.x))/100 * negy
                    self.ball.xinc = sqrt(self.ball.v ** 2 - self.ball.yinc ** 2) * negx
                                
                if self.ball.x > self.x + self.width // 2:
                    self.ball.yinc = self.ball.baseSpeed * (100 - 0.25 * (self.ball.x-self.x)) /100 * negy
                    self.ball.xinc = sqrt(self.ball.v ** 2 - self.ball.yinc**2) * negx

    def drawRacket(self):
        self.screen.blit(self.images[int(self.state)%3], (self.x, self.y))
        self.state += 0.01

class Game:
    def __init__(self, width = 600, height = 800):
        self.screen = pg.display.set_mode((width, height))
        self.ball = Ball(self.screen, (255,255,0))
        self.racket = Racket(self.screen, self.ball)
        self.background = pg.image.load(r".\resources\background.jpg")
        self.balls = []
        self.bricks = []
        self.generateBricks()
        self.newLevel = True
        self.level = 0
        self.font = None
        self.lives = 3
        self.levels = {1: (), 
                       2:(5,11,17,23,29,35,41), 
                       3: (5,11,17,23,29,35,41,6,7,8,9,10,18,19,20,21,22,30,31,32,33,34)
                       }
        self.game_over = False
        #self.clock = pg.time.Clock()
            
    def generateBricks(self):
        for i in range(42):
            self.bricks.append(Brick((i*100)%600, 100 + i//6*50, self.screen))
    
    def checkVictory(self):
        defeatedBricks = 0
        for brick in self.bricks:
            if brick.status == False:
                defeatedBricks += 1
            if defeatedBricks >= 42:
                self.newLevel = True
            
    
    def resetPositions(self):
        
        self.racket.x = self.screen.get_width() // 2 - self.racket.width // 2
        self.racket.y = self.screen.get_height() - 50
        self.ball.xinc = 0
        self.ball.yinc = 0
        self.ball.v = 0
        self.ball.x = self.screen.get_width() // 2
        self.ball.y = self.racket.y -10 - 1
        

    def levelControl(self):
        if self.newLevel == True:
                if self.level == 0:
                   cover = pg.image.load("resources\cover.jpg")
                   self.screen.blit(cover, (0,0))
                   coverLoop = True
                   while coverLoop:
                       self.screen.blit(cover, (0,0))
                       pg.display.flip()
                       eventList = pg.event.get()
                       for event in eventList:
                        if event.type == pg.QUIT:
                            self.game_over = True
                        if event.type == pg.KEYDOWN:
                           if event.key == pg.K_SPACE:
                               coverLoop = False
                               
                self.level += 1
                self.screen.fill((0,0,0))
                self.font = pg.font.Font("freesansbold.ttf", 32)
                if self.level in self.levels:
                    text = self.font.render("LEVEL {}".format(self.level), True, (255,255,255))
                    self.screen.blit(text, (self.screen.get_rect().centerx - text.get_rect().centerx , self.screen.get_rect().centery - text.get_rect().centery))
                    pg.display.flip()
                    pg.time.wait(2000)
                    self.resetPositions()
                    for brick in self.bricks:
                        brick.status = True
                    for i in self.levels[self.level]:
                        self.bricks[i].status = False                    
                    self.newLevel = False
                else:
                    text = self.font.render("YOU SAVED THE MULTIVERSE!!!!!", True, (255,255,255))
                    self.screen.blit(text, (self.screen.get_rect().centerx - text.get_rect().centerx , self.screen.get_rect().centery - text.get_rect().centery))
                    pg.display.flip()
                    pg.time.wait(2000)
                    self.game_over = True

    def writeLivesLevel(self):
        self.font = pg.font.Font("freesansbold.ttf", 32)
        textLives = self.font.render("LIVES {}".format(self.lives), True, (255,255,255))
        textLevel = self.font.render("LEVEL {}".format(self.level), True, (255,255,255))
        self.screen.blit(textLives, (0,0))
        self.screen.blit(textLevel, (self.screen.get_width() - textLevel.get_rect().width, 0))
        
    def checkGameOver(self):
        if self.game_over == True:
               playMore = True 
               while playMore:
                   eventList = pg.event.get()
                   for event in eventList:
                       if event.type == pg.QUIT:
                            playMore = False
                       if event.type == pg.KEYDOWN:
                           if event.key == pg.K_SPACE:
                               self.game_over = False
                               playMore = False
                               self.level = 0
                               self.lives = 3
                           if event.key == pg.K_x:
                               playMore = False

                   self.screen.fill((0,0,0))
                   self.font = pg.font.Font("freesansbold.ttf", 32)
                   text = self.font.render("GAME OVER".format(self.level), True, (255,255,255))
                   text2 = self.font.render("X to Quit Space to Continue".format(self.level), True, (255,255,255))
                   self.screen.blit(text, (self.screen.get_rect().centerx - text.get_rect().centerx , self.screen.get_rect().centery - text.get_rect().centery))
                   self.screen.blit(text2, (self.screen.get_rect().centerx - text2.get_rect().centerx , 100))
                   pg.display.flip()
 
    def main_loop(self):
                    
        while not self.game_over:
            #self.clock.tick(60)
            
            #Check stuff
            self.levelControl()
            self.checkVictory()
            self.ball.calculateSpeed()
            self.racket.checkBallHitsRacket()
            self.ball.updatePos()

            if self.ball.dead == True:
                self.resetPositions()
                self.lives -= 1
                self.ball.dead = False
            
            if self.lives == 0:
                self.game_over = True
            
            #Events and Key presses (includes cheats!)
            eventList = pg.event.get()

            if pg.key.get_pressed()[pg.K_RIGHT]:
                    self.racket.moveRacket("R")
                               
            if pg.key.get_pressed()[pg.K_LEFT]:
                    self.racket.moveRacket("L")
                                   
            for event in eventList:
                if event.type == pg.QUIT:
                    self.game_over = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and self.ball.v == 0:
                        self.ball.xinc += 0.2
                        self.ball.yinc -= 0.2
                    if event.key == pg.K_0 and self.ball.v == 0:
                        for brick in self.bricks:
                            brick.status = False
                    if event.key == pg.K_1 and self.ball.v == 0:
                        for i in range(42):
                            if i % 2 != 0:       
                                self.bricks[i].status = False
                    if event.key == pg.K_2 and self.ball.v == 0:
                        for i in range(42):
                            if (i//6) % 2 != 0:       
                                self.bricks[i].status = False
                    if event.key == pg.K_3 and self.ball.v == 0:
                        for i in (5,11,17,23,29,35,41):
                            self.bricks[i].status = False 
            
            #Draw everything
            
            self.screen.blit(self.background, (0,0))         
            for brick in self.bricks:
                brick.checkCrash(self.ball)
                if brick.status == True:
                    pg.draw.rect(self.screen, brick.color, brick)
                        
            self.writeLivesLevel()
            self.racket.drawRacket()
            self.ball.drawBall()
            pg.display.flip()
            
            #Check Game Over
            self.checkGameOver()

if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()

