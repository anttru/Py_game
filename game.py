from numpy import tan, sqrt
from random import randint
import pygame as pg

class Ball:
    def __init__(self, screen : pg.Surface, x, y, color = (255,255,255), radius = 10, xinc = 0, yinc = 0):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.radius = radius
        self.xinc = xinc
        self.yinc = yinc
        self.v = sqrt(self.yinc**2 + self.xinc**2)
    def updatePos(self):
        if self.x > (self.screen.get_width() - self.radius) or self.x < (0 +self.radius):
            self.xinc *= -1
        if self.y > (self.screen.get_height() - self.radius) or self.y < (0 +self.radius):
            self.yinc *= -1
        self.x += self.xinc
        self.y += self.yinc
    def drawBall(self):
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

class Brick(pg.Rect):
    def __init__(self, x, y, screen):
        pg.Rect.__init__(self, x, y, 100, 50)
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.status = True
        self.screen = screen
    def checkCrash(self, ball : Ball):
        if self.x < ball.x < self.x +100 and ((self.y+40 < ball.y < self.y +50) or (self.y < ball.y < self.y +10)) and self.status == True:
            ball.yinc *= -1
            self.status = False
        if self.y < ball.y < self.y +50 and ((self.x + 95 < ball.x < self.x +100) or (self.x < ball.x < self.x +5)) and self.status == True:
            ball.xinc *= -1
            self.status = False
    def drawBrick(self):
        pg.draw.rect(self.screen, self.color, self)

class Racket:
    def __init__(self, screen, x, y, ball : Ball):
        self.x = x
        self.y = y
        self.v = 0.2
        self.screen = screen
        self.color = (255,255,255)
        self.width = 100
        self.rect = pg.Rect(self.x, self.y, self.width, 10)
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
        self.rect.update(self.x, self.y, self.width, 10)
    
    def checkBallHitsRacket(self):
        if ((self.x + self.width -5 < self.ball.x < self.x + self.width) or (self.x < self.ball.x < self.x + 5)) and (self.y < self.ball.y < self.y + 10):
                self.ball.xinc *= -1
        if (self.x < self.ball.x < self.x +self.width) and (self.y < self.ball.y < self.y + 10):
                self.ball.yinc *= -1
                if self.ball.xinc < 0:
                    negx = -1
                else:
                    negx = 1
                if self.ball.yinc < 0:
                    negy = -1
                else:
                    negy = 1
                if self.ball.x < self.x + self.width//2:
                    self.ball.yinc = 0.2*(75+0.5*(self.ball.x-self.x))/100 * negy
                    self.ball.xinc = sqrt(self.ball.v**2 - self.ball.yinc**2) * negx
                                
                if self.ball.x > self.x + self.width//2:
                    self.ball.yinc = 0.2*(100 - 0.25*(self.ball.x-self.x))/100 * negy
                    self.ball.xinc = sqrt(self.ball.v**2 - self.ball.yinc**2) * negx
    
    def drawRacket(self):
        pg.draw.rect(self.screen, self.color, self.rect)

class Game:
    def __init__(self, width = 600, height = 800):
        self.screen = pg.display.set_mode((width, height))
        self.ball = Ball(self.screen, width // 2, height -61, (255,255,0))
        self.racket = Racket(self.screen, width//2-50, height - 50, self.ball)
        self.balls = []
        self.bricks = []
        self.generateBricks()
        #for i in range(randint(0,20)):
        #   self.balls.append(Ball(self.screen, randint(0,600), randint(0, 800), (randint(0,255),randint(0,255),randint(0,255)), randint(5,20), xinc=random(), yinc=(random())))
    
    def generateBricks(self):
        for i in range(42):
            self.bricks.append(Brick((i*100)%600, 100 + i//6*50, self.screen))
        
    def main_loop(self):
        game_over = False
        
        while not game_over:
            
            eventList = pg.event.get()
            
            self.ball.v = sqrt(self.ball.yinc**2 + self.ball.xinc**2)
            
            if pg.key.get_pressed()[pg.K_RIGHT]:
                    self.racket.moveRacket("R")
                               
            if pg.key.get_pressed()[pg.K_LEFT]:
                    self.racket.moveRacket("L")
            
            self.racket.checkBallHitsRacket()            
                       
            for event in eventList:
                if event.type == pg.QUIT:
                    game_over = True
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
            self.screen.fill((255,0,0))
            #for ball in self.balls:
            #    ball.drawBall()
            #    ball.updatePos()
            for brick in self.bricks:
                brick.checkCrash(self.ball)
                if brick.status == True:
                    pg.draw.rect(self.screen, brick.color, brick)
              
            self.racket.drawRacket()
            self.ball.drawBall()
            self.ball.updatePos()
            pg.display.flip()
            



if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
