#!/usr/bin/env python

import pygame as pg
import random, math, sys

#Globals
w=int(1680/2)
h=int(1050/2)
p2m=2*2.0e9/h #OM of Callisto's semiMajorAxis divided by the height of the screen
m2p=1.0/p2m
G=6.67300e-11
dt=60 #60 seconds should be good enough for euler integration

#Pygame setup stuff
pg.init()
pg.display.set_caption("Gravity Simulation of Jupiter and the Galilean Moons by Emmett Hart adapted from Ian Millet")

Info=pg.display.Info()
#Screen = pygame.display.set_mode((w,h),pygame.FULLSCREEN)
Screen = pg.display.set_mode((w,h))
x,y = Screen.get_size()


Space = pg.Surface((w,h))
Space.fill((0,0,0))
Space.set_colorkey((0,0,0))


#Jupiter
jupiterDiameter=142800000 # meters
jmass=1.8986e27 #kg
jdp=int(jupiterDiameter*m2p);
jupiterSurface=pg.transform.scale(pg.image.load('jupiter.jpg').convert(),(jdp,jdp))


Particles = []
class Particle:
    def __init__(self,x,y,speedx,speedy,mass,radius,Color=(255,255,255)):
        self.x = x
        self.y = y
        self.speedx = speedx
        self. speedy = speedy
        self.mass = mass
        self.radius = radius
        self.color = Color

Moons     = []
class Moon(Particle):
    #Everything in SI units
    def __init__(self,parentParticle,mass,semiMajorAxis,color=(255,255,255),radius=3*p2m):
        mu=parentParticle.mass*G
        vo=math.sqrt(mu/semiMajorAxis)
        Particle.__init__(self, parentParticle.x,parentParticle.y+semiMajorAxis,vo,0,mass,radius,color)
    def xp(self):
        return self.x*m2p
    def yp(self):
        return self.y*m2p
    def radiusp(self):
        return self.radius*m2p


imass=8.93e22   #kg
emass=4.8e22    #kg
gmass=1.48e23   #kg
cmass=1.08e23   #kg

ia =  421800e3 #m
ea =  671100e3 #m
ga =  1070400e3 #m
ca =  1882700e3 #m


iT =  1.769 # days
eT =  3.551 # days
gT =  7.155 # days
cT =  16.69 # days

jupiter=Particle(w/2*p2m,h/2*p2m,0,0,jmass,jupiterDiameter);
Particles.append(jupiter)

Moons.append(Moon(jupiter,imass,ia,(100, 100,  0))) #Io
Moons.append(Moon(jupiter,emass,ea,(222,184,135))) #Europa
Moons.append(Moon(jupiter,gmass,ga,( 50, 50, 50))) #Ganymede
Moons.append(Moon(jupiter,cmass,ca,(100,100,150))) #Callisto

#Better way to do this?
for M in Moons:
   Particles.append(M)

def Move():
    for P in Particles:
        for P2 in Particles:
            if P != P2:
                XDiff = P.x - P2.x
                YDiff = P.y - P2.y
                Distance = math.sqrt((XDiff**2)+(YDiff**2))
                #if Distance < 10: Distance = 10
                #F = (G*M*M)/(R**2)
                Force = G*(P.mass*P2.mass)/(Distance**2)
                #F = M*A  ->  A = F/M
                Acceleration = Force / P.mass
                XComponent = XDiff/Distance
                YComponent = YDiff/Distance
                P.speedx -= Acceleration * XComponent*dt
                P.speedy -= Acceleration * YComponent*dt
    for P in Particles:
        P.x += P.speedx*dt
        P.y += P.speedy*dt


def Draw():
    Space.fill((0,0,0))
    Screen.fill((0,0,0))
    Screen.blit(jupiterSurface,(w/2-jdp/2,h/2-jdp/2))
    for M in Moons:
       pg.draw.circle(Space, M.color, (int(M.xp() ),int(h-M.yp())), int(round(M.radiusp())))
    Screen.blit(Space,(0,0))
    pg.display.flip()

def GetInput():
    keystate = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keystate[pg.K_ESCAPE]:
           pg.quit(); sys.exit()
        elif event.type == pg.KEYDOWN:
           if event.key == pg.K_F11:
             pg.display.toggle_fullscreen()


def main():
    while True:
        GetInput()
        Move()
        Draw()

if __name__ == '__main__': main()
