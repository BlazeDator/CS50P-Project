import pygame, sys

class Debug_text:
   def __init__(self,font:pygame.font.Font, text:str="1", x:int=0, y:int=0, color:tuple=(255,255,255), background:tuple=(0,0,0)):
      self.text = text
      self.color = color
      self.background = background
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
   def __init__(self, size:int=30, screen_center=(), speed:int=8, pcolor:tuple=(255,255,255)):
      self.surface = pygame.Surface((size,size)) 
      self.rect = pygame.draw.circle(surface=self.surface, color=pcolor, center=(self.surface.get_width()/2, self.surface.get_height()/2), radius=self.surface.get_width()/2, width=0)
      self.rect.move_ip(screen_center[0]-size, screen_center[1]-size)
      self.speed = speed
      self.speed_diag = c_diag_speed(self.speed)
      self.mov_vector = [0, 0]

   def movement(self, keys):
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

def main():
   # Initialization
   pygame.init()
   screen_size = 1280, 720
   screen = pygame.display.set_mode(screen_size)
   clock = pygame.time.Clock()
   max_framerate = 200
   font = pygame.font.Font('freesansbold.ttf', 32)
   delta = 0

   # Colors
   black = 0, 0, 0
   white = 255,255,255
   red = 255, 0, 0

   # player
   player = Player(screen_center=(screen_size[0]/2, screen_size[1]/2))


   # Debug Info
   show_debug = False
   debug_info = Debug_text(font)
   debug_framerate = Debug_text(font, y=32)
   debug_delta = Debug_text(font, y=64)
   debug_player_x = Debug_text(font, y=96)
   debug_player_y = Debug_text(font, y=128)
   debug_player_speed = Debug_text(font, y=160)
   
   # For Blitting
   debug = [
      debug_info,
      debug_framerate,
      debug_delta,
      debug_player_x,
      debug_player_y,
      debug_player_speed
      ]


   # Game Loop
   while True:  
      delta += clock.tick(max_framerate) 
      
      for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()
      
      keys = pygame.key.get_pressed()
      player.movement(keys)

      if delta >= 25: # 40 Tick Rate Updates
         player.rect.move_ip(*player.mov_vector)  # Player Movement       
         delta = 0


      
      # Background
      screen.fill(black)
      # Draw Image
      screen.blit(player.surface, player.rect)


      # Framerate Control
      if keys[pygame.K_UP]:
         max_framerate += 5
      if keys[pygame.K_DOWN]:
         max_framerate -= 5

      # Debug  Info
      if keys[pygame.K_F3]:
         show_debug = True
      if show_debug:
         debug_info.update("V0.1")
         debug_framerate.update(str(int(clock.get_fps())) + " Max FPS: " + str(max_framerate))
         debug_delta.update(str(clock.get_time())+" ms")
         debug_player_x.update("player X: " + str(player.rect.x))
         debug_player_y.update("player Y: " + str(player.rect.y))
         debug_player_speed.update("Speed: " + str(player.mov_vector))
         for info in debug:
            screen.blit(info.surface, info.rect)
         if keys[pygame.K_F4]:
            show_debug = False  

      # Send Frame
      pygame.display.update()

   
def c_diag_speed(speed: int) -> float:
   # return speed * 0.7071
   v1, v1.x, v1.y = pygame.math.Vector2(), 0, 0
   v2, v2.x, v2.y = pygame.math.Vector2(), speed, speed
   return v1.distance_to(v2) / 2




if __name__ == "__main__":
    main()