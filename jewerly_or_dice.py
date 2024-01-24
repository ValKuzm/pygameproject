import pygame, sys

pygame.init()
# задаем размер экрана, заголовок и задний фон
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Menu')

BG = pygame.image.load('BG.jpg')
first_level_bg = pygame.image.load('first.jpg')
second_level_bg = pygame.image.load('second.jpg')

white = (255, 255, 255)

# класс, отвечающий за кнопки
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        if self.image is None:
            self.image = self.text
            
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# класс, описывающий персонажа игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect(center=(x, y))
        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.enemyes = pygame.sprite.Group()

# класс, отвечающий за стены
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, weight, height):
        super().__init__()

        self.image = pygame.Surface([weight, height])
        self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# класс отвечающий за сокровища
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(center=(x, y))

# в данной функции подводятся итоги игры, которые записываются в файл result.txt
def end(score):
    pygame.display.set_caption('The End')
    while True:
        SCREEN.fill((0,0,0))
        end_text = f"Congratulations! You finished the game with {score} points!!"
        end_window_rect = SCREEN.get_rect(center=(1280 // 2, 720 // 2))

        font = pygame.font.Font(None, 30)
        text = font.render(end_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(1280 // 2, 720 // 2 - 50))

        SCREEN.blit(SCREEN, end_window_rect)
        SCREEN.blit(text, text_rect)

        pygame.display.update()

        try:
            with open('results.txt', 'r') as f:
                count = len(list(map(str.strip, f.readlines())))
        except FileNotFoundError:
            count = 0
        with open('results.txt', 'w') as f:
            f.write(f'Игра №{count}: вы заработали {score} очков')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# используем файл, в котором записаны нужные нам цвета и шрифты
def get_font(size):
    return pygame.font.Font("font.ttf", size)

# экран, где пользователь выбирает уровень
def play():
    pygame.display.set_caption('Play')

    while True:
        SCREEN.fill('black')

        # задаем новый заголовок
        play_mouse_pos = pygame.mouse.get_pos()
        play_text = get_font(100).render('CHOOSE LEVEL', True, '#b68f40')
        play_rect = play_text.get_rect(center=(640, 100))

        # создаем новые кнопки
        first_button = Button(image=pygame.image.load('rect.png'), pos=(640, 340),
                             text_input='FIRST LEVEL', font=get_font(40), base_color='#d7fcd4', hovering_color='White')
        
        second_button = Button(image=pygame.image.load('rect.png'), pos=(640, 540),
                              text_input='SECOND LEVEL', font=get_font(40), base_color='#d7fcd4', hovering_color='White')

        SCREEN.blit(play_text, play_rect)
        for button in [first_button, second_button]:
            button.change_color(play_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if first_button.check_for_input(play_mouse_pos):
                    first_level()
                elif second_button.check_for_input(play_mouse_pos):
                    second_level()

        pygame.display.update()

# первый уровень
def first_level():
    pygame.display.set_caption('First level')
    
    # группы спрайтов
    wall_list = pygame.sprite.Group()
    PLAYER = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    # координаты стен
    wall_coord = [
        [0, 0, 10, 720],
        [10, 0, 1270, 10],
        [1270, 10, 10, 710],
        [10, 710, 1270, 10],
        [10, 110, 768, 10],
        [878, 10, 10, 240],
        [248, 250, 640, 10],
        [110, 220, 10, 350],
        [10, 570, 110, 10],
        [238, 250, 10, 350],
        [420, 360, 10, 350],
        [430, 360, 530, 10],
        [520, 460, 10, 250],
        [530, 460, 530, 10],
        [1050, 92, 10, 378],
        [1200, 92, 10, 478],
        [770, 570, 500, 10]
    ]

    for coord in wall_coord:
        wall = Wall(coord[0], coord[1], coord[2], coord[3])
        wall_list.add(wall)
        all_sprites.add(wall)
        
    # задаем расположение игрока и сокровищ
    player = Player(50, 50, 'yodo.png')
    PLAYER.add(player)
    all_sprites.add(player)
    player.walls = wall_list

    diamond = Coin(850, 50, 'diamond.png')
    all_sprites.add(diamond)
    coins.add(diamond)

    gold = Coin(300, 680, 'goldi.png')
    all_sprites.add(gold)
    coins.add(gold)

    coin = Coin(1250, 50, 'coin.png')
    all_sprites.add(coin)
    coins.add(coin)

    clock = pygame.time.Clock()
    fps = 60
    speed = 3
    score = 0
    number = 3

    while True:
        SCREEN.blit(first_level_bg, (0, 0))
        SCREEN.blit(player.image, player.rect)
        all_sprites.draw(SCREEN)
        pygame.display.update()
        
        player_coin = pygame.sprite.spritecollide(player, coins, True)
        if player_coin:
            score += 100
            number -= 1
            
        bloock_hit_list = pygame.sprite.spritecollide(player, wall_list, False)
        if bloock_hit_list:
            number = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= speed
            if player.rect.x < 0:
                player.rect.x = 0
                
        elif keys[pygame.K_RIGHT]:
            player.rect.x += speed
            if player.rect.x > 1260:
                player.rect.x = 1260
                
        elif keys[pygame.K_DOWN]:
            player.rect.y += speed
            if player.rect.y > 710:
                player.rect.y = 710
                
        elif keys[pygame.K_UP]:
            player.rect.y -= speed
            if player.rect.y < 0:
                player.rect = 10

        clock.tick(fps)
        pygame.display.update()

        if number == 0:
            end(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# второй уровень
def second_level():
    pygame.display.set_caption('Second level')
    wall_list = pygame.sprite.Group()
    PLAYER = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    wall_coord = [
        [0, 0, 10, 720],
        [10, 0, 1270, 10],
        [1270, 10, 10, 710],
        [10, 710, 1270, 10],
        [60, 80, 10, 210],
        [70, 110, 378, 10],
        [608, 60, 10, 200],
        [70, 170, 428, 10],
        [498, 120, 10, 60],
        [508, 120, 50, 10],
        [670, 10, 10, 300],
        [120, 310, 560, 10],
        [760, 80, 10, 310],
        [850, 80, 10, 310],
        [770, 800, 420, 10],
        [1190, 60, 10, 310],
        [1020, 360, 170, 10],
        [950, 100, 10, 450],
        [150, 450, 1160, 10],
        [60, 450, 10, 190],
        [70, 545, 350, 10],
        [420, 545, 10, 165],
        [770, 650, 10, 60],
        [770, 640, 400, 10],
        [1170, 640, 10, 70]
    ]

    for coord in wall_coord:
        wall = Wall(coord[0], coord[1], coord[2], coord[3])
        wall_list.add(wall)
        all_sprites.add(wall)

    player = Player(35, 40, 'yodo.png')
    PLAYER.add(player)
    all_sprites.add(player)
    player.walls = wall_list

    diamond = Coin(850, 550, 'diamond.png')
    all_sprites.add(diamond)
    coins.add(diamond)

    gold = Coin(300, 500, 'goldi.png')
    all_sprites.add(gold)
    coins.add(gold)

    coin = Coin(900, 50, 'coin.png')
    all_sprites.add(coin)
    coins.add(coin)

    clock = pygame.time.Clock()
    fps = 60
    speed = 3
    score = 0
    number = 3

    while True:
        SCREEN.blit(second_level_bg, (0, 0))
        SCREEN.blit(player.image, player.rect)
        all_sprites.draw(SCREEN)
        pygame.display.update()
        player.walls = wall_list
        
        player_coin = pygame.sprite.spritecollide(player, coins, True)
        if player_coin:
            score += 100
            number -= 1
            
        bloock_hit_list = pygame.sprite.spritecollide(player, wall_list, False)
        if bloock_hit_list:
            number = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= speed
            if player.rect.x < 0:
                player.rect.x = 0
                
        elif keys[pygame.K_RIGHT]:
            player.rect.x += speed
            if player.rect.x > 1260:
                player.rect.x = 1260
                
        elif keys[pygame.K_DOWN]:
            player.rect.y += speed
            if player.rect.y > 710:
                player.rect.y = 710
                
        elif keys[pygame.K_UP]:
            player.rect.y -= speed
            if player.rect.y < 0:
                player.rect = 10

        clock.tick(fps)
        pygame.display.update()
        if number == 0:
            end(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# главное меню, при нажатии единственной кнопки "Play" появляется "новый" экран (старый заполняется черным цветом, появляются новые кнопки)
def main_menu():
    pygame.display.set_caption('Menu')

    while True:
        SCREEN.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render('MAIN MENU', True, '#b68f40')
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load('rect.png'), pos=(640, 340),
                             text_input='PLAY', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button]:
            button.change_color(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()

        pygame.display.update()

main_menu()
