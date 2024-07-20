import pygame
import random

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('SpaceShip.png'),(90,90))
        self.rect =self.image.get_rect(center=(200,300))
        self.vel = 5

        
class Bullet(pygame.sprite.Sprite):

    def __init__(self, SpaceShip):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('laserBullet.png'),(40,40))
        self.rect = self.image.get_rect()
        # self.image.fill((255,0,0))
        self.rect.centerx = SpaceShip.rect.centerx 
        self.rect.centery = SpaceShip.rect.centery
        self.VEL = 3

    def update(self):
        self.rect.y -= self.VEL
        if(self.rect.y < 20):
            self.kill()

class Enemy(pygame.sprite.Sprite):

    def __init__(self,Game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('enemy.png'),(50,50))
        self.rect = self.image.get_rect()
        # self.image.fill((255,255,0))
        self.VEL = 1

    def update(self):
        self.rect.y += self.VEL
        if(self.rect.y > 550):
            self.kill()
  
        

class Game:
    def __init__(self):
        self.end = False
        self.done = False
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.image = pygame.transform.scale( pygame.image.load('Space.png'),(self.width,self.height))
        
        self.score = 0
        self.health = 3
    
        pygame.font.init()
        self.font = pygame.font.Font('slkscrb.ttf',20)
        self.text = self.font.render('SCORE: '+str(self.score),True,(101,101,150))   
         
        self.textrect = self.text.get_rect()
        self.textrect.center = (60,30)

        self.health_bar = pygame.transform.scale(pygame.image.load("hearts.png"),(150,110))

        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self.player = SpaceShip()
        self.all_sprites.add(self.player)

    def handle_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.end = True
            elif event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end=True
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player)
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)
        
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.player.rect.x - self.player.vel > 0:
            self.player.rect.x -= self.player.vel
        if keys_pressed[pygame.K_d] and self.player.rect.x + self.player.vel + self.player.rect.width <self.width:
            self.player.rect.x += self.player.vel
        if keys_pressed[pygame.K_w] and self.player.rect.y + self.player.vel > 0:
            self.player.rect.y -= self.player.vel
        if keys_pressed[pygame.K_s] and self.player.rect.y + self.player.vel + self.player.rect.height < self.height:
            self.player.rect.y += self.player.vel
        
        if random.randint(1,max(3,200 - self.score)) == 1:
                
            e = Enemy(self)
            e.rect.x = random.randint(5,550)
            e.rect.y = random.randint(-10,0)
            
            self.enemies.add(e)
            self.all_sprites.add(e)
        if pygame.sprite.groupcollide(self.enemies,self.bullets,True,True):
            self.score+=1
        for en in self.enemies:
            if(self.player.rect.colliderect(en.rect)):
                self.health -= 1
                if self.health == 0:
                    file_content = open("HS.txt",'r').read()
                    file_write = open("HS.txt",'w')
                    file_write.write(str(max(int(file_content),self.score)))
                    file_write.close()
                    score = self.score
                    self.end=True
                    
                tempP = SpaceShip()
                self.all_sprites.add(tempP)
                self.player.kill()
                self.player = tempP
                if(self.health == 2):
                    self.health_bar = pygame.transform.scale(pygame.image.load("hearts2.png"),(150,110)) 
                else:
                    self.health_bar = pygame.transform.scale(pygame.image.load("hearts1.png"),(150,110))
    def update(self):
        self.all_sprites.update()

        
    def draw_win(self):
        self.screen.blit(self.image,(0,0))
        self.text = self.font.render('SCORE: {}'.format(self.score),True,(101,101,150))
        self.screen.blit(self.health_bar,(470,-20))
        self.screen.blit(self.text,self.textrect)
        self.all_sprites.draw(self.screen)        
        pygame.display.update()

    def draw_over(self):
        pygame.init()
        screen = pygame.display.set_mode((700,500))    
        pygame.display.set_caption("Game Over!")
        image= pygame.transform.scale(pygame.image.load("Space.png"),(700,500))
        pygame.font.init()
        font = pygame.font.Font('slkscrb.ttf',50)
        game_over = font.render('Game Over',True,(160,50,50))
        restart = pygame.font.Font('slkscrb.ttf',18).render("(Q to Quit   |   R to Restart)",True,(144,144,144))
        sc = pygame.font.Font('slkscrb.ttf',25).render("Score: "+ str(self.score),True,(144,144,20))
        file = open("HS.txt",'r').read()
        hsc = pygame.font.Font('slkscrb.ttf',25).render("HighScore: "+file,True,(144,144,20))

        active = 1
        while active:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.done=0
                    active = 0
                    
                elif event.type ==  pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE  or event.key == pygame.K_q:
                        self.done=0
                        active=0
                    if event.key == pygame.K_r:
                        self.done=1
                        active=0
            screen.blit(image,(0,0))
            screen.blit(game_over,(180,30))
            screen.blit(restart,(175,350))
            screen.blit(sc,(150,200))
            screen.blit(hsc,(330,200))
            pygame.display.update()
            





def main():
    pygame.init()
    game = Game()
    pygame.display.set_caption("Space shooters")
    clock = pygame.time.Clock()
    while not game.end:
        game.handle_events()
        game.update()
        game.draw_win()
        clock.tick(60)
    game.draw_over()
    if game.done :
        main()



if __name__ == "__main__":
    main()
    pygame.quit()
