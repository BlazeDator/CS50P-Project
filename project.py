import pygame, sys, random

class Debug_text:
   def __init__(self,font:pygame.font.Font, text:str="1", x:int=0, y:int=0, color:list=[255,255,255], background:list=[0,0,0]):
      self.text = text
      self.color = pygame.color.Color(*color)
      self.background = pygame.color.Color(*background)
      self.font = font
      self.surface = self.font.render(self.text, True, self.color, self.background)
      
      self.x = x
      self.y = y
      self.rect = self.surface.get_rect()
      self.rect.move_ip(self.x, self.y)

   def update(self, text:str):
      self.text = text
      self.surface = self.font.render(self.text, True, self.color, self.background)

class Player:
   def __init__(self, size:int=30, screen_center=(1280,720), speed:int=10, pcolor:list=[255,255,255]):
      self.surface = pygame.Surface((size,size)) 
      self.color = pygame.color.Color(*pcolor)
      self.rect = pygame.draw.circle(surface=self.surface, color=self.color, center=(self.surface.get_width()/2, self.surface.get_height()/2), radius=self.surface.get_width()/2, width=0)
      self.rect.move_ip(screen_center[0]-size, screen_center[1]-size)
      self.speed = speed
      self.speed_diag = calc_diag_speed(self.speed)
      self.mov_vector = [0, 0]

   def movement(self, keys):
      # Directionals
      if keys[pygame.K_w]:
         self.mov_vector = [0, -self.speed]
      if keys[pygame.K_s]:
         self.mov_vector = [0, self.speed]
      if keys[pygame.K_a]:
         self.mov_vector = [-self.speed, 0]
      if keys[pygame.K_d]:
         self.mov_vector = [self.speed, 0] 

      # Diagonals
      if keys[pygame.K_w] and keys[pygame.K_a]: 
         self.mov_vector = [-(self.speed_diag), -(self.speed_diag)]
      if keys[pygame.K_w] and keys[pygame.K_d]: 
         self.mov_vector = [(self.speed_diag), -(self.speed_diag)]
      if keys[pygame.K_s] and keys[pygame.K_a]: 
         self.mov_vector = [-(self.speed_diag), (self.speed_diag)]
      if keys[pygame.K_s] and keys[pygame.K_d]: 
         self.mov_vector = [(self.speed_diag), (self.speed_diag)]

      #Still
      if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
         self.mov_vector = [0, 0]

   def move(self):
      self.rect.move_ip(*self.mov_vector)

   def check_death(self, squares:list):
      for square in squares:
         if self.rect.colliderect(square.rect):
            self.speed, self.speed_diag = 0, 0

class Square(Player):
   def __init__(self, size:int=20, speed:int=5, screen_size:tuple=(1280,720), pcolor:list=[255,0,0]):
      self.surface = pygame.Surface((size,size))
      self.color = pygame.color.Color(*pcolor)
      self.surface.fill(self.color)
      self.rect = self.surface.get_rect()
      self.speed = speed
      self.speed_diag = calc_diag_speed(self.speed)
      self.mov_vector = [0, 0]
      # Spawn
      x = random.randint(0, screen_size[0]-size)
      y = random.randint(0, screen_size[1]-size)
      self.rect.move_ip(x, y)
      self.keys = {
         pygame.K_w : True,
         pygame.K_a : True,
         pygame.K_s : True,
         pygame.K_d : True
      }
   
   def mov_random(self):
      for key in self.keys:
         rnd = random.choice([True,False])
         if rnd:
            self.keys[key] = rnd
         else:
            self.keys[key] = rnd
      self.movement(self.keys)

   def mov_player(self, player_x:int, player_y:int):
      s_x = self.rect.x
      s_y = self.rect.y

      self.keys = {key : False for key in self.keys}

      if s_x < player_x:
         self.keys[pygame.K_d] = True
      elif s_x > player_x:
         self.keys[pygame.K_a] = True
      else:
         self.keys[pygame.K_d] = False
         self.keys[pygame.K_a] = False

      if s_y < player_y:
         self.keys[pygame.K_s] = True
      elif s_y > player_y:
         self.keys[pygame.K_w] = True
      else:
         self.keys[pygame.K_s] = False
         self.keys[pygame.K_w] = False
      self.movement(self.keys)
      
   def check_collisions(self, squares:list):
      for next in squares:
         if self.rect.x == next.rect.x and self.rect.y == next.rect.y:
            pass
         elif self.rect.colliderect(next.rect):
            if self.rect.x <= next.rect.x:
               self.mov_vector[0] += -self.speed
            elif self.rect.x  > next.rect.x:
               self.mov_vector[0] += +self.speed

            if self.rect.y  <= next.rect.y:
               self.mov_vector[1] += -self.speed
            elif self.rect.y  > next.rect.y:
               self.mov_vector[1] += self.speed
      

def main():
   # Initialization
   pygame.init()
   pygame.display.set_caption("Survival Squared V0.1")
   icon = pygame.Surface((32,32))
   icon.fill((255, 0, 0))
   pygame.display.set_icon(icon)
   screen_size = 1600, 900
   screen = pygame.display.set_mode(screen_size)
   clock = pygame.time.Clock()
   max_framerate = 200
   font = pygame.font.Font('freesansbold.ttf', 32)


   # Colors
   black = [0, 0, 0]
   white = [255,255,255]
   red = [255, 0, 0]
   green = [0,255,0]
   blue = [0,0,255]
   purple = [150,20,255]

   
   # player
   player = Player(screen_center=(screen_size[0]/2, screen_size[1]/2))

   # Squares
   squares_red = [Square(screen_size=screen_size, speed=5, pcolor=red) for i in range(25)]
   squares_green = [Square(screen_size=screen_size, speed=1, pcolor=green) for i in range(25)]
   squares_blue = [Square(screen_size=screen_size, speed=8, pcolor=blue) for i in range(10)]
   squares_purple = [Square(screen_size=screen_size, speed=6, pcolor=purple) for i in range(5)]

   # Timers
   delta_25_ms = 0   # 40  Ticks per second
   delta_1000_ms = 0 # 1   Tick  per second
   start = False

   # Debug Info
   show_debug = False
   def update_debug() -> list[str]:
      debug_info = [
               "Version 0.1 ",
               "Player Vector: " + str(player.mov_vector),
               str(int(clock.get_fps())) + " Max FPS: " + str(max_framerate),
               str(clock.get_time())+" ms",
               "Player X: " + str(player.rect.x),
               "Player Y: " + str(player.rect.y),
               "Delta 1s: " + str(delta_1000_ms),
               "Squares: " + str(len(squares_red)+len(squares_green)+len(squares_blue))
            ]
      return debug_info
   debug_info = update_debug()
   lines = len(debug_info) * 32
   debug = [Debug_text(font, y=i) for i in range(0,lines,32)]
   
   # Game Loop
   while True:  
      tick = clock.tick(max_framerate) 
      delta_25_ms += tick
      delta_1000_ms += tick

      for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()
      
      keys = pygame.key.get_pressed()

      if keys[pygame.K_SPACE]:
         start = True
      if keys[pygame.K_BACKSPACE]:
         start = False
         player.speed = 10
         player.speed_diag = calc_diag_speed(player.speed)

      player.movement(keys)
 
      entities = squares_red + squares_green + squares_blue + squares_purple
      if delta_25_ms >= 25: # 40 Tick Rate Updates
         player.move() # Player Movement
         player.check_death(entities)
         if start:
            for square in squares_red: # Squares Movement
               square.mov_player(player.rect.x, player.rect.y)
               square.check_collisions(squares_red + squares_green + squares_blue + squares_purple)
               square.move()
            for square in squares_green:
               square.mov_player(player.rect.x, player.rect.y)
               square.check_collisions(squares_red + squares_green + squares_blue)
               square.move()
            for square in squares_blue:
               square.mov_player(player.rect.x, player.rect.y)
               square.check_collisions(squares_blue + squares_green)
               square.move()
            for square in squares_purple:
               square.check_collisions(squares_red + squares_green + squares_blue + squares_purple)
               square.move()

         delta_25_ms = 0

      if delta_1000_ms >= 1000: # 1 Tick Rate Updates
         for square in squares_purple:
            square.mov_player(player.rect.x, player.rect.y)
         delta_1000_ms = 0

      
      # Background
      screen.fill(black)
      # Draw Image
      screen.blit(player.surface, player.rect)
      for square in squares_red:
         screen.blit(square.surface, square.rect)
      for square in squares_green:
         screen.blit(square.surface, square.rect)
      for square in squares_blue:
         screen.blit(square.surface, square.rect)
      for square in squares_purple:
         screen.blit(square.surface, square.rect)

      # Framerate Control
      if keys[pygame.K_UP]:
         max_framerate += 5
      if keys[pygame.K_DOWN]:
         max_framerate -= 5

      # Debug  Info
      if keys[pygame.K_F3]:
         show_debug = True
      if show_debug:
         debug_info = update_debug()
         for i in range(len(debug)):
            debug[i].update(debug_info[i])
            screen.blit(debug[i].surface, debug[i].rect)
         if keys[pygame.K_F4]:
            show_debug = False  

      # Send Frame
      pygame.display.update()

   
def calc_diag_speed(speed: int) -> float:
   # return speed * 0.7071
   v1, v1.x, v1.y = pygame.math.Vector2(), 0, 0
   v2, v2.x, v2.y = pygame.math.Vector2(), speed, speed
   return v1.distance_to(v2) / 2




if __name__ == "__main__":
    main()