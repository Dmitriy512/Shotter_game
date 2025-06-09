#Создай собственный Шутер!
from random import randint
from pygame import *
win_width = 700
win_heihgt = 500 
window = display.set_mode((win_width, win_heihgt))
display.set_caption('pygame window')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_heihgt))

lost = 0
score = 0

clock = time.Clock()
FPS = 60

font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 80)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fires = mixer.Sound('fire.ogg')

bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_heihgt:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win = font2.render('You win!', True, (255, 215, 0))
lose = font2.render('You lose!', True, (255, 215, 0))

rocket = Player('rocket.png', 300, 400, 100, 90, 5)
monsters = sprite.Group()

for i in range(1,6):
    monster = Enemy('ufo.png', randint(100, 600), 10, 100, 50, randint(1, 3))
    monsters.add(monster)

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                fires.play()
    if finish != True:
        window.blit(background, (0, 0))
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        monsters.update()
        bullets.update()
        rocket.update()
        sprites_list_1 = sprite.spritecollide(rocket, monsters, False)
        sprites_list_2 = sprite.groupcollide(monsters, bullets, True, True)
        for c in sprites_list_2:
            score += 1
            monster = Enemy('ufo.png', randint(100, 600), 10, 100, 50, randint(1, 3))
            monsters.add(monster)
        
        if score >= 10:
            finish = True
            window.blit(win, (235, 220))
        
        if lost >= 3:
            finish = True
            window.blit(lose, (235, 220))

    text_score = font1.render('Счёт: ' + str(score), True, (255, 255, 255))
    text_lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        
    window.blit(text_score, (10, 20))
    window.blit(text_lose, (10, 50))

    clock.tick(FPS)
    display.update()


