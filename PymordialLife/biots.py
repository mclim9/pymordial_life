import random
import math
import copy 		#for objects

########################################################################
### Define colors
########################################################################
BiotMinSize = 40
BiotMaxSize = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0,0,255)
Colors = [RED,GREEN,GREEN,BLUE,WHITE]

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
      #self.BodyMatX = [[0 for x in range(self.symmetry)] for y in range(LegSegs)] 
      #self.BodyMatY = [[0 for x in range(self.symmetry)] for y in range(LegSegs)] 
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
      self.angleRot += 0.03 if self.angleRot > 6.28318 else -6.28318
      
      #pygame.draw.circle(screen, self.colorOut, [int(self.x),int(self.y)], int(self.size), 1)
      for i in range(0,self.symmetry):          #Draw Leg
         stopX = self.x
         stopY = self.y
         for j in range(0,LegSegs):             #Draw Leg Segment
            startX = stopX                      #Start at last point
            startY = stopY                      #Start at last point
            stopX = startX + self.BodyMatX[i][j]
            stopY = startY + self.BodyMatY[i][j]
            pygame.draw.aalines(screen, self.color[j], False, [(startX, startY), (stopX, stopY)], 2)

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
   if dist < p1.size + p2.size:
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
      #p1.angleRot += .6
      #p2.angleRot += .6
      
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
