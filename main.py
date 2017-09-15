"""
 This example shows having multiple balls bouncing around the screen at the
 same time. You can hit the space bar to spawn more balls.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 http://www.petercollingridge.co.uk/book/export/html/6
"""
########################################################################
### User Inputs
########################################################################
ScrWid = 1000
ScrHeight = 600
BALL_SIZE = 25
elasticity = 1.0

########################################################################
### Code Begin
########################################################################
import pygame
import random
import math

########################################################################
### Define colors
########################################################################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0,0,255)
Colors = [RED,(255,163,0),(255,255,0),GREEN,BLUE,WHITE]
########################################################################
### Definitions
########################################################################
class Biot:    
   ###Class to keep track of a ball's location and vector.
   def __init__(self):
      self.size  = BALL_SIZE
      self.x = random.randrange(self.size, ScrWid - self.size)
      self.y = random.randrange(self.size, ScrHeight - self.size)
      self.color = random.choice(Colors)
      #		self.speed = random.randrange(1, 3)
      self.speed = 3
      self.angleMove = random.uniform(0, math.pi*2)
      self.angleRot = random.uniform(0, math.pi*2)
      self.symmetry = random.randint(3, 9)
	  
   def move(self):
      self.x += int(math.sin(self.angleMove) * self.speed)
      self.y -= int(math.cos(self.angleMove) * self.speed)

   def bounce(self):
      if self.x > ScrWid - self.size:
         self.x = 2*(ScrWid - self.size) - self.x
         self.angleMove = - self.angleMove

      elif self.x < self.size:
         self.x = 2*self.size - self.x
         self.angleMove = - self.angleMove

      if self.y > ScrHeight - self.size:
         self.y = 2*(ScrHeight - self.size) - self.y
         self.angleMove = math.pi - self.angleMove

      elif self.y < self.size:
         self.y = 2*self.size - self.y
         self.angleMove = math.pi - self.angleMove
         
   def draw(self, screen):
      self.angleRot += 0.03
      #pygame.draw.circle(screen, self.color, [int(self.x),int(self.y)], self.size, 4)
      for i in range(0,self.symmetry):
         newX = int(self.x + self.size * math.sin(self.angleRot + (2 * math.pi * i)/self.symmetry))
         newY = int(self.y + self.size * math.cos(self.angleRot + (2 * math.pi * i)/self.symmetry))
         pygame.draw.lines(screen, self.color, False, [(self.x,self.y), (newX, newY)], 2)

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
      if speed1 > 5:
         speed1 = 5
      if speed2 > 5:
         speed1 = 5

      (p1.angleMove, p1.speed) = (angle1, speed1)
      (p2.angleMove, p2.speed) = (angle2, speed2)

      p1.x += math.sin(angle)
      p1.y -= math.cos(angle)
      p2.x -= math.sin(angle)
      p2.y += math.cos(angle)
      p1.angleRot +=  .6
      p2.angleRot +=  .6

def findBiot(biots, x, y):
    for p in biots:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None
########################################################################
### Main Code
########################################################################
def main():
   pygame.init()
   size = [ScrWid, ScrHeight]
   screen = pygame.display.set_mode(size)
   pygame.display.set_caption("Bouncing Balls")
   done = False
   selected_biot = None
   clock = pygame.time.Clock()    # Manage screen updates


   biot_List = []
   for i in range(0,30):
      biot_List.append(Biot())

   ####################################################################
   ### Main Code
   ####################################################################
   while not done:
      ################################################################
      ### Event Processing
      ################################################################
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            done = True
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:	 # Space bar! Spawn a new ball.
               biot_List.append(Biot())
            elif event.key == pygame.K_d:
               del biot_List[0]
         elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_biot = findBiot(biot_List, mouseX, mouseY)
         elif event.type == pygame.MOUSEBUTTONUP:
            selected_biot = None
      
       
      ################################################################
      ### Game Logic
      ################################################################
      for i, CurrBiot in enumerate(biot_List):
         CurrBiot.move()
         CurrBiot.bounce()
         for Biot2 in biot_List[i+1:]:
            collide(CurrBiot, Biot2)

      if selected_biot:
         (mouseX, mouseY) = pygame.mouse.get_pos()
         dx = mouseX - selected_biot.x
         dy = mouseY - selected_biot.y
         selected_biot.angle = 0.5*math.pi + math.atan2(dy, dx)
         selected_biot.speed = math.hypot(dx, dy) * 0.1
         
      ################################################################
      ### Drawing Code
      ################################################################
      screen.fill(BLACK)      # Set the screen background
      for ball in biot_List:
         ball.draw(screen)
      # --- Wrap-up
      clock.tick(60)			   # Limit to 60 frames per second
      pygame.display.flip() 	# update the screen with what we've drawn.
      
   #End While
   pygame.quit()
 
if __name__ == "__main__":
    main()
