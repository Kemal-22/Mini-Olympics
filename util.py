import pygame


class Button:
    def __init__(self, image, position, callback=None):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.callback = callback
        self.position_x = position[0]
        self.position_y = position[1]

    def check_click_and_change_state(self, current_state, new_state, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and self.is_hovering():
                current_state.change_state(new_state)
                if self.callback is not None:
                    self.callback()
                return True

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and self.is_hovering():
                return True

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def get_image_height(self):
        return self.image.get_height()

    def get_image_width(self):
        return self.image.get_width()

    def resize(self, percentage_of_original):
        width = self.get_image_width()
        height = self.get_image_height()
        scale = percentage_of_original / 100
        self.image = pygame.transform.scale(self.image, (round(width * scale), round(height * scale)))
        self.rect = self.image.get_rect()

    def move(self, position_x, position_y):
        self.rect.center = (position_x, position_y)

    def set_button_image(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.position_x, self.position_y)

    def is_hovering(self):
        mouse = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse[0], mouse[1])


class Image:
    def __init__(self, image, position):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position_x = position[0]
        self.position_y = position[1]

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def get_image_height(self):
        return self.image.get_height()

    def get_image_width(self):
        return self.image.get_width()

    def set_width(self, new_width):
        aspect_ratio = (self.get_image_height() / self.get_image_width())
        new_height = new_width * aspect_ratio
        self.image = pygame.transform.scale(self.image, (round(new_width), round(new_height)))

    def resize(self, percentage_of_original):
        width = self.get_image_width()
        height = self.get_image_height()
        scale = percentage_of_original / 100
        self.image = pygame.transform.scale(self.image, (round(width * scale), round(height * scale)))
        self.rect = self.image.get_rect()

    def move(self, position_x, position_y):
        self.rect.center = (position_x, position_y)

    def set_image(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.position_x, self.position_y)


class State:
    def __init__(self):
        self.state = "main_menu"
        self.prev_state = None

    def change_state(self, state):
        self.state = state


def save_discipline(discipline):
    f = open("discipline.txt", "w")
    f.write(discipline)
    f.close()


def read_discipline():
    f = open("discipline.txt", "r")
    discipline = f.read()
    f.close()
    return discipline


def save_country(player_flag, ID):
    if ID == 1:
        f = open("player1_flag.txt", "w")
        f.write(player_flag.name_list[player_flag.current_image])
        f.close()
    elif ID == 2:
        f = open("player2_flag.txt", "w")
        f.write(player_flag.name_list[player_flag.current_image])
        f.close()


def load_country(ID):
    if ID == 1:
        f = open("player1_flag.txt", "r")
        country = f.read()
        f.close()
        return country

    elif ID == 2:
        f = open("player2_flag.txt", "r")
        country = f.read()
        f.close()
        return country


class Text:
    def __init__(self, text: str, position, font, font_size=48, color=(25, 25, 25), antialiasing=True):
        self.text = text
        self.font_size = font_size
        self.font_name = font
        self.font = pygame.font.Font(font, self.font_size)
        self.color = color
        self.antialiasing = antialiasing
        self.text_surface = self.font.render(self.text, self.antialiasing, self.color)

        self.rect = self.text_surface.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

        self.position = (position[0], position[1])

    def render(self, screen):
        position = (round(self.rect.center[0] - self.rect.width / 2), round(self.rect.center[1] - self.rect.height / 2))
        screen.blit(self.text_surface, position)

    def recalculate(self):
        self.text_surface = self.font.render(self.text, self.antialiasing, self.color)
        self.rect = self.text_surface.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.center = (self.position[0], self.position[1])

    def set_text(self, new_text: str):
        self.text = new_text
        self.recalculate()

    def set_color(self, new_color: (int, int, int)):
        self.color = new_color
        self.recalculate()

    def set_font(self, font_name: str):
        self.font_name = font_name
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.recalculate()

    def set_font_size(self, font_size: int):
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.recalculate()

    def set_position(self, position: (int, int)):
        self.position = position
        self.recalculate()

    def set_antialiasing(self, antialiasing: bool):
        self.antialiasing = antialiasing
        self.recalculate()

    def bold(self, bold: bool):
        self.font.set_bold(bold)
        self.recalculate()

    def italic(self, italic: bool):
        self.font.set_italic(italic)
        self.recalculate()

    def underline(self, underline: bool):
        self.font.set_underline(underline)
        self.recalculate()
