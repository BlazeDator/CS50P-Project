import pygame, sys

class debug_text:
   def __init__(self,font:pygame.font.Font, text:str="1", x:int=0, y:int=0, color:tuple=(255,255,255), background:tuple=(0,0,0), size:int=32):
      self.text = text
      self.x = x
      self.y = y
      self.color = color
      self.background = background
      self.size = size
      self.font = font
      
      self.surface = self.font.render(self.text, True, self.color, self.background)
      self.rect = self.surface.get_rect()
      self.rect.move_ip(self.x, self.y)

   def update(self, text:str):
      self.text = text
      self.surface = self.font.render(self.text, True, self.color, self.background)

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

   # dot Properties
   dot = pygame.Surface((25,25))
   dot.fill(white)
   dot_rect = dot.get_rect()
   dot_rect.x = 500
   dot_rect.y = 250
   speed = 8
   speed_diag = c_diag_speed(speed) 
   dot_vector = [0, 0]

   # Debug Info
   show_debug = True
   debug_framerate = debug_text(font)
   debug_delta = debug_text(font, y=32)
   debug_player_x = debug_text(font, y=64)
   debug_player_y = debug_text(font, y=96)
   debug_player_speed = debug_text(font, y=128)
   debug_player_info = debug_text(font, y=160)
   # For Blitting
   debug = [
      debug_framerate,
      debug_delta,
      debug_player_x,
      debug_player_y,
      debug_player_speed,
      debug_player_info
      ]


   # Game Loop
   while True:  
      delta += clock.tick(max_framerate) 
      
      # Debug 
      if show_debug:
         debug_framerate.update(str(int(clock.get_fps())) + " Max FPS: " + str(max_framerate))
         debug_delta.update(str(clock.get_time())+" ms")
         debug_player_x.update("Dot X: " + str(dot_rect.x))
         debug_player_y.update("Dot Y: " + str(dot_rect.y))
         debug_player_speed.update("Speed: " + str(dot_vector))
         debug_player_info.update(str(c_diag_speed(speed)))


      for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()
      
      keys = pygame.key.get_pressed()
      
      if delta >= 25: # 40 Tick Rate Actions
         dot_rect.move_ip(*dot_vector)         
         delta = 0

      # Directionals
      if keys[pygame.K_w]:
         dot_vector = [0, -speed]
      if keys[pygame.K_s]:
         dot_vector = [0, speed]
      if keys[pygame.K_a]:
         dot_vector = [-speed, 0]
      if keys[pygame.K_d]:
         dot_vector = [speed, 0] 

      # Diagonals
      if keys[pygame.K_w] and keys[pygame.K_a]: 
         dot_vector = [-(speed_diag), -(speed_diag)]
      if keys[pygame.K_w] and keys[pygame.K_d]: 
         dot_vector = [(speed_diag), -(speed_diag)]
      if keys[pygame.K_s] and keys[pygame.K_a]: 
         dot_vector = [-(speed_diag), (speed_diag)]
      if keys[pygame.K_s] and keys[pygame.K_d]: 
         dot_vector = [(speed_diag), (speed_diag)]

      #Still
      if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
         dot_vector = [0, 0]

      # Framerate Control
      if keys[pygame.K_UP]:
         max_framerate += 5
      if keys[pygame.K_DOWN]:
         max_framerate -= 5
      if keys[pygame.K_F3]:
         show_debug = True
      if keys[pygame.K_F4]:
         show_debug = False  

      screen.fill(black)
      screen.blit(dot, dot_rect)

      # Debug
      if show_debug:
         for info in debug:
            screen.blit(info.surface, info.rect)

      pygame.display.update()

   
def c_diag_speed(speed: int) -> float:
   # return speed * 0.7071
   v1, v1.x, v1.y = pygame.math.Vector2(), 0, 0
   v2, v2.x, v2.y = pygame.math.Vector2(), speed, speed
   return v1.distance_to(v2) / 2


if __name__ == "__main__":
    main()