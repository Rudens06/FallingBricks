import pygame
import time
import random
from network.network import Network
from player import Player
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Bricks")

BG = pygame.transform.scale(pygame.image.load("./bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VELOCITY = 3

FONT = pygame.font.SysFont("San Francisco", 30)

def draw(player, player2, elapsed_time, stars):
  WIN.blit(BG, (0,0))
  
  time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
  WIN.blit(time_text, (10,10))
  
  player.draw(WIN)
  player2.draw(WIN)
  
  for star in stars: 
    pygame.draw.rect(WIN, "black", star)
  
  pygame.display.update()

def main():
  run = True
  n = Network()
  start_pos = decode_pos(n.get_pos())
  
  player = Player(start_pos[0], start_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT, (0,255,0))
  player2 = Player(0,0,PLAYER_WIDTH, PLAYER_HEIGHT, (255, 0, 0))
  
  clock = pygame.time.Clock()
  
  start_time = time.time()
  elapsed_time = 0
  
  star_add_increment = 2000
  star_count = 0
  stars = []
  hit = False
    
  while run:
    star_count += clock.tick(60)
    elapsed_time = time.time() - start_time
    
    p2pos = decode_pos(n.send(encode_pos((player.x, player.y))))
    player2.x = p2pos[0]
    player2.y = p2pos[1]
    player2.update()
    
    if star_count > star_add_increment:
      for _ in range(3):
        star_x = random.randint(0, WIDTH - STAR_WIDTH)
        star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
        stars.append(star)
      
      star_add_increment = max(200, star_add_increment - 50)
      star_count = 0
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break
    
    for star in stars[:]:
      star.y += STAR_VELOCITY
      if star.y > HEIGHT:
        stars.remove(star)
      elif star.y + STAR_HEIGHT>= player.y and star.colliderect(player):
        stars.remove(star)
        hit = True
        break
    
    if hit:
      lost_text = FONT.render("You lost!", 1, "black")
      WIN.blit(lost_text, 
              (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
      pygame.display.update()
      pygame.time.delay(3000)
      break
            
    player.move()
    draw(player, player2, elapsed_time, stars)
      
  pygame.quit()
  
# Network logic
def decode_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def encode_pos(tup):
    return str(tup[0]) + "," + str(tup[1])
  
if __name__ == "__main__":
  main()