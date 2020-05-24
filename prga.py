import pygame
from pygame import *
from random import randint


# подгружаем отдельно функции для работы со шрифтом
font.init()
# во время игры пишем надписи размера 36
font = font.Font(None, 30)
font2 = pygame.font.Font(None, 25)
# нам нужны такие картинки:
img_win = "uw.jpg"  # фон победы
img_los = "gameover.png"  # фон проигрыша
img_back = "back.jpg"  # фон игры
ramka = "ramk.png"
img_bullet = "bullets.png"  # пуля
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # враг
boss = "ufoboss.png" # boss
life = "life.png" # здоровье
star = "star.png" # звездочки
puli = "puli.png" # патроны
record = 0 # рекорд
score = 0  # сбито кораблей
goal = 1000  # столько кораблей нужно сбить для победы
lost = 0  # пропущено кораблей
max_lost = 3  # проиграли, если пропустили столько
PULI = 50 # начальное кол-во пуль

life = transform.scale(image.load(life), (25,25))

def lefezh():
    if lost == 0:
        window.blit(life, (15, 70))
        window.blit(life, (40, 70))
        window.blit(life, (65, 70))
    if lost == 1:
        window.blit(life, (15, 70))
        window.blit(life, (40, 70))
    if lost == 2:
        window.blit(life, (15, 70))


# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 15:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 8 , self.rect.top, 15, 20, -15)
        bullets.add(bullet)


# класс спрайта-врага
class Enemy(GameSprite):

    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -10
            lost = lost + 1

class Star(GameSprite):
    # движение
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

# класс спрайта-пули
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()


# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ramka = transform.scale(image.load(ramka), (700,550) )
# создаем спрайты
ship = Player(img_hero, 150, win_height - 100, 60, 80, 10)

# создание группы спрайтов-врагов
# спавн боса
hp = 100
BOSSES = sprite.Group()
BOSS = Enemy(boss, 300, -40, 100, 100, 1)
BOSSES.add(BOSS)
# функция босса
def boss():
    if score == 50:
        text = font.render("Health " + str(hp), 1, (255, 255, 255))
        window.blit(text, (300, 10))
        BOSSES.update()
        BOSSES.draw(window)

# спавн врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(15, win_width - 80), -80, 60, 60, randint(1, 5))
    monsters.add(monster)
def MONSTRI():
    if score != 50:
        monsters.update()
        monsters.draw(window)

# спавно звезд
stars = sprite.Group()
for i in range(1, 3):
    star1 = Star(star, randint(150, win_width - 80), -40, 40, 30, randint(1, 5))
    stars.add(star1)

# функция звезд ( когда они начинают падать)
def STARS():
    if lost >= 1:
        stars.update()
        stars.draw(window)

# спавн патронов
pulis = sprite.Group()
for i in range(1, 2):
    puli1 = Star(puli, randint(150, win_width - 80), -40, 40, 55, randint(1, 5))
    pulis.add(puli1)

bullets = sprite.Group()

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
FINISH = True
# Основной цикл игры:
run = True  # флаг сбрасывается кнопкой закрытия окна
while run:
    # перебираем полученные события
    for e in event.get():
        # событие нажатия на кнопку Закрыть
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if PULI > 0:
                    ship.fire()
                    PULI -= 1

    # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        # обновляем фон
        window.blit(background, (0, 0))
        window.blit(ramka, (0, -40))
        # логика рекорда
        if score > record:
            record = score
        # пишем текст на экране
        text = font.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (15, 10))
        text = font2.render("Рекорд: " + str(record), 1, (255, 255, 255))
        window.blit(text, (15, 40))
        text = font2.render("Пули: " + str(PULI), 1, (255, 255, 255))
        window.blit(text, (15, 100))
        # производим движения спрайтов
        ship.update()
        bullets.update()
        pulis.update()
        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        bullets.draw(window)
        pulis.draw(window)
        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            img = image.load(img_win)
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

        # проверяем рекорд и в зависимости от него выбираем, что должны проверять
        if score != 50:
            # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                # этот цикл повторится столько раз, сколько монстров подбито
                score = score + 1
                monster = Enemy(img_enemy, randint(15, win_width - 80), -80, 60,60, randint(1, 5))
                monsters.add(monster)
        else:
            colliders = sprite.groupcollide(BOSSES, bullets, True, True)
            for d in colliders:
                # этот цикл повторится столько раз, сколько монстров подбито
                hp -= 1
                BOSSES.add(BOSS)
                if hp <= 0:
                    score += 1
        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True  # проиграли, ставим фон и больше не управляем спрайтами.
            FINISH = False
            # при подборе звезд увеличивается хп
        if sprite.spritecollide(ship, stars, True):
            lost -=1
            star1 = Star(star, randint(150, win_width - 80), -40, 40, 30, randint(1, 5))
            stars.add(star1)
            # при подборе патронов увеличивается кол-во пуль
        if sprite.spritecollide(ship, pulis, True):
            PULI += randint(20, 50)
            puli1 = Star(puli, randint(150, win_width - 80), -40, 40, 55, randint(1, 5))
            pulis.add(puli1)
        # проверяем функцию
        boss()
        # проверяем функцию
        lefezh()
        # проверяем функцию
        STARS()
        # проверяем функцию
        MONSTRI()
        display.update()

    if not FINISH:
        img = image.load(img_los)
        d = img.get_width() // img.get_height()
        window.blit(transform.scale(img, (500, 300)), (80, 70))
        text = font.render("Для рестарта нажмите ESC " , 1, (255, 255, 255))
        window.blit(text, (200, 350))
        RUN = True
        while RUN:
            for e in event.get():
                if e.type == QUIT:
                    run = False
                    RUN = False
                    FINISH = True
                # событие нажатия на пробел - спрайт стреляет
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        score = 0
                        goal = 100
                        lost = 0
                        max_lost = 3
                        PULI = 50
                        ship = Player(img_hero, 150, win_height - 100, 60, 80, 10)
                        monsters = sprite.Group()
                        for i in range(1, 6):
                            monster = Enemy(img_enemy, randint(110, win_width - 80), -40, 60, 60, randint(1, 5))

                            monsters.add(monster)
                        ship.update()
                        monsters.update()
                        bullets.update()
                        ship.reset()
                        monsters.draw(window)
                        bullets.draw(window)

                        finish = False
                        RUN = False
                        FINISH = True
            display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)