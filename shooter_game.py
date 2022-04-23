#Создай собственный Шутер!

from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('Star Wars Shooter')
background = transform.scale(image.load('deathstar.jpg'), (700, 500))
class Sprites(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, x_size, y_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (x_size, y_size))
        self.speed = player_speed
        self.x_size = x_size
        self.y_size = y_size
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(Sprites):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x <= 635:
            self.rect.x += self.speed
    def fire(self):
        lazer1 = Bullet('lazer.png', self.rect.left, self.rect.centery, 10, 20, 30)
        lazer2 = Bullet('lazer.png', self.rect.right, self.rect.centery, 10, 20, 30)
        bullets.add(lazer1)
        bullets.add(lazer2)
class Enemy(Sprites):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y>=500:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            lost += 1
class Bullet(Sprites):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<=0:
            self.kill()
player = Player('x-wing.png', 300,  400, 5, 70, 70)
TIE = sprite.Group()
for a in range(6):
    enemy1 = Enemy('TIE.png', randint(0, 600), 0, randint(1, 3), 90, 70)
    TIE.add(enemy1)
bullets = sprite.Group()
mixer.init()
mixer.music.load('StarWars.ogg')
mixer.music.set_volume(0.2)
mixer.music.play(loops=-1)
clock = time.Clock()
FPS = 60
game = True
finish = False
score = 0
lost = 0
font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 60)
fire_music = mixer.Sound('XWing fire.ogg')
fire_music.set_volume(0.1)
while game:
    for e in event.get():
        if e.type==QUIT:
            game = False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                player.fire()
                fire_music.play()
            if e.key==K_r:
                finish = False
                for i in TIE:
                    i.kill()
                score = 0
                lost = 0
                for x in range(6):
                    enemy1 = Enemy('TIE.png', randint(0, 600), 0, randint(1, 3), 90, 70)
                    TIE.add(enemy1)
                
    if finish!=True:
        window.blit(background, (0, 0))
        text = font1.render("Score: "+str(score), True, (255, 255, 255))
        textpos = 10, 20
        text2 = font1.render('Lost: '+str(lost), True, (255, 255, 255))
        textpos2 = 10, 55
        player.reset()
        player.update()
        bullets.draw(window)
        bullets.update()
        TIE.draw(window)
        TIE.update()
        sprites_list1 = sprite.spritecollide(player, TIE, False)
        sprites_list2 = sprite.groupcollide(bullets, TIE, True, True)
        window.blit(text, textpos)
        window.blit(text2, textpos2)
        if lost>=5:
            finish = True
            text3 = font2.render('You lose', True, (255, 255, 255))
            window.blit(text3, (170, 200))
        if score>=30:
            finish = True
            text3 = font2.render('You win', True, (255, 255, 255))
            window.blit(text3, (170, 200))
        if len(sprites_list1)>=1:
            finish = True
            text3 = font2.render('You lose', True, (255, 255, 255))
            window.blit(text3, (170, 200))
        for collide in sprites_list2:
            score+=1
            enemy = Enemy('TIE.png', randint(0, 600), 0, randint(3, 4), 90, 70)
            TIE.add(enemy)
    clock.tick(FPS)
    display.update()
