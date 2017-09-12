"""
 This example shows having multiple balls bouncing around the screen at the
 same time. You can hit the space bar to spawn more balls.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""
########################################################################
### User Inputs
########################################################################
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
BALL_SIZE = 25
 
########################################################################
### Code Begin
########################################################################
import pygame
import random

########################################################################
### Define colors
########################################################################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE  = (0,0,255)
RED = (255, 0, 0)
 
########################################################################
### Definitions
########################################################################
class Ball:    
    ###Class to keep track of a ball's location and vector.
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
 
def make_ball():
    ### Function to make a new, random ball.
    ball = Ball()
    # Starting position of the ball.
    # Don't spawn on the edge 
    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)
 
    # Speed and direction of rectangle
    ball.change_x = random.randrange(-2, 3)
    ball.change_y = random.randrange(-2, 3)
 
    return ball
 
########################################################################
### Main Code
########################################################################
def main():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
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
        for CurrBall in ball_list:
            # Move the ball's center
            CurrBall.x += CurrBall.change_x
            CurrBall.y += CurrBall.change_y
 
            # Wall Boundary
            if CurrBall.y > SCREEN_HEIGHT - BALL_SIZE or CurrBall.y < BALL_SIZE:
                CurrBall.change_y *= -1
            if CurrBall.x > SCREEN_WIDTH - BALL_SIZE or CurrBall.x < BALL_SIZE:
                CurrBall.change_x *= -1

            # Hitting Other Balls 
            #for ball in ball_list:

        ################################################################
        ### Drawing Code
        ################################################################
        screen.fill(BLACK)      # Set the screen background
        for ball in ball_list:
            pygame.draw.circle(screen, BLUE, [ball.x, ball.y], BALL_SIZE)
 
        # --- Wrap-up
        clock.tick(60)			# Limit to 60 frames per second
        pygame.display.flip() 	# update the screen with what we've drawn.
         
    #End While
    pygame.quit()
 
if __name__ == "__main__":
    main()
