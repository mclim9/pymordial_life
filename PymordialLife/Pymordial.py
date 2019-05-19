########################################################################
### Python based physics simulation based on
### Jason Spafford's Primordial Life Screensaver
########################################################################
###
### Date: 2017.09.11
### Author: Martin C Lim
### Version: 0.1
### Description: Biots float in a petri dish.  Each organism is composed
###   of several segmented legs.  Colors define function:
###   -Green Generates energy
###   -Red   Takes energy from others
###   -Blue  Pro
###   -White Sheild
###
### Links: 
###   http://programarcadegames.com/
###   http://simpson.edu/computer-science/c
###   http://www.petercollingridge.co.uk/book/export/html/6
###
### Special thanks to Peter Collingridge at:
###   http://www.petercollingridge.co.uk/
########################################################################
### User Inputs
########################################################################
ScrWid = 1200
ScrHeight = 700
BiotMinSize = 40
BiotMaxSize = 60
BiotRotate = 0
elasticity = 1.0  #Biot bounce speed increase
MaxSpeed = 4      #Maximum biot speed.
LegSegs = 5       #Number of leg segments
StartEnergy = 400 #Biot Start Energy
CCost = 40        #Collision Cost
Colli = [0,1,0]
########################################################################
### Code Begin
########################################################################
import pygame
#from biots import *
import random
import math
import copy       #for objects
import pickle     #Object saving
import time

########################################################################
### Define colors
########################################################################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0,0,255)
Colors = [RED,GREEN,GREEN,BLUE,WHITE]

from pygame.locals import *
#flags = FULLSCREEN | DOUBLEBUF
flags = DOUBLEBUF
#screen = pygame.display.set_mode(resolution, flags, bpp)

########################################################################
### Definitions
########################################################################
class Biot:    
   ###Class to keep track of a ball's location and vector.
   def __init__(self):
      self.root = random.randint(BiotMinSize,BiotMaxSize)
      self.x = random.randrange(self.root, ScrWid - self.root)
      self.y = random.randrange(self.root, ScrHeight - self.root)
      self.energy = StartEnergy
      #		self.speed = random.randrange(1, 3)
      self.speed = 3
      self.angleMove = random.uniform(0, math.pi*2)
      self.angleRot = random.uniform(0, math.pi*2)
         
      ### Leg Section   
      self.symmetry = random.randint(3, 9)
      self.angleSeg = []
      self.color = []
      for i in range(0,LegSegs):
         self.angleSeg.append(random.uniform(0, math.pi*2))
         self.color.append(random.choice(Colors))
      
      ### Calc Biot true size
      self.colorOut = BLACK
      self.size = 0
      self.segSize = self.root/LegSegs
      
      ### PreCalc Biot Leg coordinates.
      self.BodyMatX = [[0 for x in range(LegSegs)] for y in range(self.symmetry)] 
      self.BodyMatY = [[0 for x in range(LegSegs)] for y in range(self.symmetry)] 
      for i in range(0,self.symmetry):          #Draw Leg
         stopX = self.x
         stopY = self.y
         legAngle = self.angleRot + (2*math.pi*i)/self.symmetry
         for j in range(0,LegSegs):             #Draw Leg Segment
            startX = stopX                      #Start at last point
            startY = stopY                      #Start at last point
            self.BodyMatX[i][j] = self.segSize * math.sin(legAngle + self.angleSeg[j])
            self.BodyMatY[i][j] = self.segSize * math.cos(legAngle + self.angleSeg[j])
            stopX = startX + self.BodyMatX[i][j]
            stopY = startY + self.BodyMatY[i][j] 
            hypot = math.hypot(self.x-stopX,self.y-stopY)
            if hypot > self.size:
               self.size = hypot                #Largest distance from center.
               self.colorOut = self.color[j]    #Color of outer most segment

   def move(self):
      self.x += int(math.sin(self.angleMove) * self.speed)
      self.y -= int(math.cos(self.angleMove) * self.speed)

   def bounce(self):
      if self.x > ScrWid - self.size:
         self.x = 2*(ScrWid - self.size) - self.x
         self.angleMove = -self.angleMove

      elif self.x < self.size:
         self.x = 2*self.size - self.x
         self.angleMove = -self.angleMove

      if self.y > ScrHeight - self.size:
         self.y = 2*(ScrHeight - self.size) - self.y
         self.angleMove = math.pi - self.angleMove

      elif self.y < self.size:
         self.y = 2*self.size - self.y
         self.angleMove = math.pi - self.angleMove
         
   def draw(self, screen):
      self.angleRot -= (0.03 if self.angleRot > 6.28318 else -6.28318)
      #startTime = time.time()
      #pygame.draw.circle(screen, self.colorOut, [int(self.x),int(self.y)], int(self.size), 1)
      for i in range(0,self.symmetry):          #Draw Leg
         stopX = self.x
         stopY = self.y
         legAngle = self.angleRot + (2*3.14159*i)/self.symmetry
         for j in range(0,LegSegs):             #Draw Leg Segment
            startX = stopX                      #Start at last point
            startY = stopY                      #Start at last point
            if BiotRotate:
               stopX = startX + self.BodyMatX[i][j]
               stopY = startY + self.BodyMatY[i][j]
            else:
               stopX = startX + self.segSize * math.sin(legAngle + self.angleSeg[j])
               stopY = startY + self.segSize * math.cos(legAngle + self.angleSeg[j])
            pygame.draw.lines(screen, self.color[j], False, [(startX, startY), (stopX, stopY)], 1)
      #print "draw Elapsed time: " + str(time.time()-startTime)
      
   def energyCalc(self):
      for j in range(0,LegSegs):
         self.energy += 2 if self.color[j] == GREEN else 0
         self.energy -= 1 if self.color[j] == RED   else 0
         self.energy -= 1 if self.color[j] == BLUE  else 0   
         self.energy -= 0 if self.color[j] == WHITE else 0   

def collide(p1, p2):
   dx = p1.x - p2.x
   dy = p1.y - p2.y

   dist = math.hypot(dx, dy)
   #dist = math.sqrt(dx * dx + dy * dy)
   if dist < (p1.size + p2.size):
      tangent = math.atan2(dy, dx)
      angle = 0.5 * math.pi + tangent

      angle1 = 2*tangent - p1.angleMove
      angle2 = 2*tangent - p2.angleMove
      speed1 = p2.speed*elasticity
      speed2 = p1.speed*elasticity
      speed1 = MaxSpeed if speed1 > MaxSpeed else speed1
      speed2 = MaxSpeed if speed2 > MaxSpeed else speed2
         
      (p1.angleMove, p1.speed) = (angle1, speed1)
      (p2.angleMove, p2.speed) = (angle2, speed2)

      p1.x += math.sin(angle)
      p1.y -= math.cos(angle)
      p2.x -= math.sin(angle)
      p2.y += math.cos(angle)
      p1.angleRot += .3
      p2.angleRot += .3
      
      ### Energy Calc
      p1.energy += CCost if p1.colorOut == RED else 0
      p2.energy += CCost if p2.colorOut == RED else 0
      p1.energy += 0.5*CCost if p1.colorOut == WHITE else 0
      p2.energy += 0.5*CCost if p2.colorOut == WHITE else 0
      p1.energy -= (CCost + 10)
      p2.energy -= (CCost + 10)
      

def findBiot(biots, x, y):
    for p in biots:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def saveBiots(data):
   with open("biot.dat", "wb") as f:
      pickle.dump(data, f)

def loadBiots():
   try:
      with open("biots.dat","rb") as f:
         print("trying to open")
         data = pickle.load(f)
   except:
      data = [Biot() for i in range(0,200)]
      print("No Data")
   return data
   
########################################################################
### Main Code
########################################################################
def main():
   pygame.init()
   pygame.mouse.set_visible(False)
   size = [ScrWid, ScrHeight]
   screen = pygame.display.set_mode(size,flags)
   screen.set_alpha(None)
   
   pygame.display.set_caption("Pymordial Life")
   done = False
   selected_biot = None
   clock = pygame.time.Clock()    # Manage screen updates

   ####################################################################
   ### Font
   ####################################################################
   pygame.font.init() # you have to call this at the start, 
   myfont = pygame.font.SysFont('Courier', 24, bold=True)

   #biot_List = [Biot() for i in range(0,100)]
   biot_list = []
   biot_List = loadBiots()

   ####################################################################
   ### Main Code
   ####################################################################
   while not done:
      ################################################################
      ### Event Processing
      ################################################################
      #pygame.mouse.set_visible(False)
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            done = True
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:	 # Space bar! Spawn a new ball.
               biot_List.append(Biot())
            elif event.key == pygame.K_d:
               del biot_List[0]
            elif (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
               saveBiots(biot_List)
               done = True
         elif event.type == pygame.MOUSEMOTION:
               pygame.mouse.set_visible(True)
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #    (mouseX, mouseY) = pygame.mouse.get_pos()
        #    selected_biot = findBiot(biot_List, mouseX, mouseY)
        # elif event.type == pygame.MOUSEBUTTONUP:
        #    selected_biot = None
         else:
            pass
            
      ################################################################
      ### Game Logic
      ################################################################
      for i, CurrBiot in enumerate(biot_List):
         CurrBiot.energyCalc()
         if CurrBiot.energy > 5*StartEnergy:
            CurrBiot.energy =  2*StartEnergy
            BabyBiot = copy.copy(CurrBiot)
            BabyBiot.angleMove = -CurrBiot.angleMove
            BabyBiot.x += 2.5 * CurrBiot.size
            biot_List.append(BabyBiot)
         if CurrBiot.energy < 0:
            del biot_List[i]
            
         CurrBiot.move()
         CurrBiot.bounce()
         for Biot2 in biot_List[i+1:]:
            if random.choice(Colli):
               collide(CurrBiot, Biot2)
     # if selected_biot:
     #    (mouseX, mouseY) = pygame.mouse.get_pos()
     #    dx = mouseX - selected_biot.x
     #    dy = mouseY - selected_biot.y
     #    selected_biot.angle = 0.5*math.pi + math.atan2(dy, dx)
     #    selected_biot.speed = math.hypot(dx, dy) * 0.1
         
      ################################################################
      ### Drawing Code
      ################################################################
      screen.fill(BLACK)      # Set the screen background
      for ball in biot_List:
         ball.draw(screen)
         outText = "Biots:%d FPS:%.2f"%(len(biot_List),clock.get_fps())
         textsurface = myfont.render(outText, True, (255, 255, 255)) #render
      # --- Wrap-up
      clock.tick(60)			   # Limit to 60 frames per second
      screen.blit(textsurface,(0,0))  #Draw text
      pygame.display.update() 	# update the screen with what we've drawn.
   #End While
   pygame.quit()
 
if __name__ == "__main__":
    main()
