import pygame, sys

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Menu')
BG = pygame.image.load('BG.jpg')

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

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

def play():
    pygame.display.set_caption('Play')

    while True:
        SCREEN.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def levels():
    pygame.display.set_caption('Play')

    while True:
        SCREEN.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def main_menu():
    pygame.display.set_caption('Menu')

    while True:
        SCREEN.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render('MAIN MENU', True, '#b68f40')
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load('rect.png'), pos=(640, 250),
                             text_input='PLAY', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        levels_button = Button(image=pygame.image.load('rect.png'), pos=(640, 380),
                               text_input='LEVELS', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        quit_button = Button(image=pygame.image.load('rect.png'), pos=(640, 510),
                            text_input='QUIT', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, levels_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if levels_button.change_color(menu_mouse_pos):
                    levels()
                if quit_button.change_color(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

