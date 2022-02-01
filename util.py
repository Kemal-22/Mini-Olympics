import pygame


class Button:
    def __init__(self, image, position_x, position_y, callback):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (position_x, position_y)
        self.callback = callback

    def check_click(self, current_state, new_state):
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(x, y):
                if new_state is not False:
                    current_state.state = new_state
                self.callback()
                return True

    def check_click_no_state_change(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
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


class Image:
    def __init__(self, image, position_x, position_y):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (position_x, position_y)

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
        f.write(player_flag.name_list[player_flag.currentimage])
        f.close()
    elif ID == 2:
        f = open("player2_flag.txt", "w")
        f.write(player_flag.name_list[player_flag.currentimage])
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


class Initialized:

    def __init__(self):
        self.running_initialized = False
        self.leaderboard_initialized = False
        self.jumping_initialized = False
