from re import A
import pygame as pg

pg.init()

mainscreen = pg.display.set_mode((600,800))

game_over = False
x = 300
y = 400
xinc = 0.25
yinc = 0.25
ball = pg.draw.circle(mainscreen, (255,255,0), (x,y), 10)
while not game_over:
    #procesar eventos
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            game_over = True
        
    
    #modificar objetos
    if ball.center[0] > 590 or ball.center[0] < 10:
        xinc *= -1
    if ball.center[1] > 790 or ball.center[1] < 10: 
        yinc *= -1
    x += xinc
    y += yinc
    #refrescar pantalla
    mainscreen.fill((255,0,0))
    ball = pg.draw.circle(mainscreen, (255,255,0), (x,y), 10)
    pg.display.flip()
    

pg.quit()

 
 

         




