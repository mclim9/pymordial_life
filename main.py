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
      self.x = random.randrange(BALL_SIZE, ScrWid - BALL_SIZE)
      self.y = random.randrange(BALL_SIZE, ScrHeight - BALL_SIZE)
      self.color = random.choice(Colors)
      #		self.speed = random.randrange(1, 3)
      self.speed = 3
      self.angle = random.uniform(0, math.pi*2)
      self.size  = BALL_SIZE
	  
   def move(self):
      self.x += int(math.sin(self.angle) * self.speed)
      self.y -= int(math.cos(self.angle) * self.speed)
   def bounce(self):
      if self.x > ScrWid - self.size:
         self.x = 2*(ScrWid - self.size) - self.x
         self.angle = - self.angle

      elif self.x < self.size:
         self.x = 2*self.size - self.x
         self.angle = - self.angle

      if self.y > ScrHeight - self.size:
         self.y = 2*(ScrHeight - self.size) - self.y
         self.angle = math.pi - self.angle

      elif self.y < self.size:
         self.y = 2*self.size - self.y
         self.angle = math.pi - self.angle


def collide(p1, p2):
   dx = p1.x - p2.x
   dy = p1.y - p2.y

   dist = math.hypot(dx, dy)
   if dist < p1.size + p2.size:
      tangent = math.atan2(dy, dx)
      angle = 0.5 * math.pi + tangent

      angle1 = 2*tangent - p1.angle
      angle2 = 2*tangent - p2.angle
      speed1 = p2.speed*elasticity
      speed2 = p1.speed*elasticity
      if speed1 > 5:
         speed1 = 5
      if speed2 > 5:
         speed1 = 5

      (p1.angle, p1.speed) = (angle1, speed1)
      (p2.angle, p2.speed) = (angle2, speed2)

      p1.x += math.sin(angle)
      p1.y -= math.cos(angle)
      p2.x -= math.sin(angle)
      p2.y += math.cos(angle)

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
         pygame.draw.circle(screen, ball.color, [int(ball.x),int(ball.y)], ball.size, 4)

      # --- Wrap-up
      clock.tick(60)			   # Limit to 60 frames per second
      pygame.display.flip() 	# update the screen with what we've drawn.
      
   #End While
   pygame.quit()
 
if __name__ == "__main__":
    main()
