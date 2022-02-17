from random import random, randint
import pygame as pg

class Ball:
    def __init__(self, screen : pg.Surface, x, y, color = (255,255,255), radius = 10, xinc = 0.5, yinc = 0.5):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.radius = radius
        self.xinc = xinc
        self.yinc = yinc
    def updatePos(self):
        if self.x > (self.screen.get_width() - self.radius) or self.x < (0 +self.radius):
            self.xinc *= -1
        if self.y > (self.screen.get_height() - self.radius) or self.y < (0 +self.radius):
            self.yinc *= -1
        self.x += self.xinc
        self.y += self.yinc
    def drawBall(self):
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

class Game:
    def __init__(self, width = 600, height = 800):
        self.screen = pg.display.set_mode((width, height))
        self.ball = Ball(self.screen, width // 2, height //2, (255,255,0))
        self.balls = []

        for i in range(randint(0,20)):
            self.balls.append(Ball(self.screen, randint(0,600), randint(0, 800), (randint(0,255),randint(0,255),randint(0,255)), randint(5,20), xinc=random(), yinc=(random())))
        
    def main_loop(self):
        game_over = False
        while not game_over:
            eventList = pg.event.get()
            for event in eventList:
                if event.type == pg.QUIT:
                    game_over = True
            
            self.screen.fill((255,0,0))
            for ball in self.balls:
                ball.drawBall()
                ball.updatePos()
            self.ball.drawBall()
            self.ball.updatePos()
            pg.display.flip()
            



if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
