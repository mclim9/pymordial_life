Pymordial Life
==============
Description: Petri dish life simulator inspired by Jason Spafford's 
   Primordial Life screensaver/program.  Biots float in a petri dish.  
   When they gather enough energy they reproduce.
   When they don't have enough energy, they die.
   
Colors define function:
  *Green Generates energy each cycle
  *Red   Takes energy from others upon collision
  *Blue  No action at this time.
  *White Protects biot from attack.

Degrees of Freedom: Variables that determine which biots flurish
   *Energy Cost for each line segment
   *Collision energy cost.  
      Helpful for population density control
   
Developed w/ the help of the following Links: 
   *http://programarcadegames.com/
   *http://simpson.edu/computer-science/
   *http://www.petercollingridge.co.uk/book/export/html/6

Special thanks to Peter Collingridge at:
   *http://www.petercollingridge.co.uk/

MacOS Requirements
------------------

`pygame` requires external c/c++ libraries. When installing from pip, these dependencies must be met beforehand.

Using [homebrew](https://brew.sh):

`brew install brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi`

Then you can install python dependencies as usual:

`pip install -r requirements.txt`
