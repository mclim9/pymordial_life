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
elasticity = 1.01

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
class Ball:    
	###Class to keep track of a ball's location and vector.
	def __init__(self):
		self.x = 0
		self.y = 0
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
	
 
def make_ball():
    ### Function to make a new, random ball.
    ball = Ball()
    # Starting position of the ball.
    # Don't spawn on the edge 
    ball.x = random.randrange(BALL_SIZE, ScrWid - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, ScrHeight - BALL_SIZE)
 
 
    return ball

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
		
########################################################################
### Main Code
########################################################################
def main():
    pygame.init()
    size = [ScrWid, ScrHeight]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bouncing Balls")
    done = False
    clock = pygame.time.Clock()    # Manage screen updates

 
    ball_list = []
    ball = make_ball()
    ball_list.append(ball)
 
    ####################################################################
    ### Main Code
    ####################################################################
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:	 # Space bar! Spawn a new ball.
                    ball = make_ball()
                    ball_list.append(ball)
                elif event.key == pygame.K_d:
                    del ball_list[0]                
                    
        ################################################################
        ### Game Logic
        ################################################################
        for i, CurrBall in enumerate(ball_list):
            CurrBall.move()
            CurrBall.bounce()
            for Ball2 in ball_list[i+1:]:
	       collide(CurrBall, Ball2)


        ################################################################
        ### Drawing Code
        ################################################################
        screen.fill(BLACK)      # Set the screen background
        for ball in ball_list:
            pygame.draw.circle(screen, ball.color, [int(ball.x),int(ball.y)], ball.size, 4)
 
        # --- Wrap-up
        clock.tick(60)			# Limit to 60 frames per second
        pygame.display.flip() 	# update the screen with what we've drawn.
         
    #End While
    pygame.quit()
 
if __name__ == "__main__":
    main()
