from pygame import *
from random import randint
from time import time as timer
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#шрифты и надписи
font.init()
font2 = font.SysFont('Arial', 36)


#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = 'bullet.png'
img_aster = 'asteroid.png'


score = 0 #сбито кораблей
lost = 0 #пропущено кораблей


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 
   def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -105)
        bullets.add(bullet)


class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Astro(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

num_fire = 0
rel_time = 0


font1 = font.SysFont('Arial', 72)
lose = font1.render("Проиграл ", 1, (255, 255, 255))
win = font1.render("Выиграл ", 1, (255, 255, 255))


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
max_lost = 3
goal = 10


monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()


for i in range(1, 9):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

for i in range(1, 5):
    asteroid = Astro(img_aster, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)


#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
           run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time  = timer()
                    rel_time = True

    if not finish:
       #обновляем фон
       window.blit(background,(0,0))


       #пишем текст на экране
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))


       #производим движения спрайтов
       ship.update()
       monsters.update()
       bullets.update()
       asteroids.update()


       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       asteroids.draw(window)

       if rel_time == True:
           now_time = timer()

           if now_time - last_time < 3:
               reload = font2.render('Wait, reload...', 1, (150, 0 ,0))
               window.blit(reload, (260, 460))
           else:
               num_fire = 0
               rel_time = False

       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

       if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))

       if score >= goal:
            finish = True
            window.blit(win, (200, 200))

       display.update()
    time.delay(50)
 
