import pygame
import util
import math

MAIN_FONT = "./font/PublicPixel-0W6DP.ttf"
paths = {
    "button_left": "./Assets/country_selection/button_left.png",
    "button_left_active": "./Assets/country_selection/button_left_active.png",
    "button_right": "./Assets/country_selection/button_right.png",
    "button_right_active": "./Assets/country_selection/button_right_active.png",
    "flag_background": "./Assets/country_selection/flag_background.png",
    "play_button": "./Assets/country_selection/play_button.png",
    "play_button_active": "./Assets/country_selection/play_button_active.png",
    "back_button": "./Assets/single_event_menu/backbutton.png",
    "back_button_active": "./Assets/single_event_menu/backbuttonactive.png",
    "background": "backgroundfull3.png"
}



class TimingClock:
    def __init__(self):
        self.start = pygame.time.get_ticks()

    def get_current_time_in_milliseconds(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.start

    def get_current_time_in_seconds(self):
        current_time = pygame.time.get_ticks()
        return math.floor((current_time - self.start) / 1000)


def format_word(word):
    temp = ""
    for letter in word:
        temp += letter.lower()

    temp = temp.replace('\n', '')
    temp = temp.replace(' ', '_')
    return temp


def load_flag_list():
    list_file = open("./Data/flag_list.txt", "r")
    countries_array = []
    for word in list_file:
        new_word = format_word(word)
        countries_array.append(new_word)

    return countries_array


def load_flag_names():
    list_file = open("./Data/flag_list.txt", "r")
    countries_array = []
    for word in list_file:
        word = word.replace('\n', '')
        countries_array.append(word)

    return countries_array


def load_discipline():
    pass


def load_flag_images():
    countries_array = load_flag_list()
    countries_images_array = []
    for country in countries_array:
        flag = util.Image("./Assets/flags/" + country + ".png", 100, 100)
        countries_images_array.append(flag)

    return countries_images_array


class Flag:
    def __init__(self, id):
        self.name_list = load_flag_list()
        self.images = load_flag_images()
        self.current_image = 0
        if id == 1:
            for country in self.images:
                self.pos_x = 375
                self.pos_y = 475
                country.resize(50)
                country.move(self.pos_x, self.pos_y)

        else:
            for country in self.images:
                self.pos_x = 1225
                self.pos_y = 475
                country.resize(50)
                country.move(self.pos_x, self.pos_y)
                self.current_image = 1

        self.currentimageobject = self.images[0]
        self.id = id

        self.button_left = util.Button(paths["button_left"], self.pos_x - 50, self.pos_y, None)
        self.button_left.resize(200)
        self.button_left.move(self.pos_x - 265, self.pos_y)

        self.button_right = util.Button(paths["button_right"], self.pos_x - 50, self.pos_y, None)
        self.button_right.resize(200)
        self.button_right.move(self.pos_x + 265, self.pos_y)

    def change_current_image(self, dir, other_player):
        if dir == "up" and self.current_image + 1 < len(self.name_list):
            if other_player.current_image != self.current_image + 1:
                self.current_image += 1
            elif other_player.current_image == self.current_image + 1 and self.current_image + 2 < len(self.name_list):
                self.current_image += 2
            else:
                self.current_image = 0

        elif dir == "up" and self.current_image + 1 >= len(self.name_list):
            if other_player.current_image == 0:
                self.current_image = 1
            else:
                self.current_image = 0

        elif dir == "down" and self.current_image - 1 >= 0:
            if other_player.current_image != self.current_image - 1:
                self.current_image -= 1
            elif other_player.current_image == self.current_image - 1 and self.current_image - 2 >= 0:
                self.current_image -= 2
            else:
                self.current_image = len(self.name_list) - 1

        elif dir == "down" and self.current_image - 1 <= 0:
            if other_player.current_image == len(self.name_list) - 1:
                self.current_image = len(self.name_list) - 2
            else:
                self.current_image = len(self.name_list) - 1

    def update(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.currentimageobject = self.images[self.current_image]
        self.currentimageobject.update(screen)

        if self.button_left.is_hovering():
            self.button_left.set_button_image(paths["button_left_active"])
            self.button_left.resize(200)
            self.button_left.move(self.pos_x - 265, self.pos_y)
        else:
            self.button_left.set_button_image(paths["button_left"])
            self.button_left.resize(200)
            self.button_left.move(self.pos_x - 265, self.pos_y)

        if self.button_right.is_hovering():
            self.button_right.set_button_image(paths["button_right_active"])
            self.button_right.resize(200)
            self.button_right.move(self.pos_x + 265, self.pos_y)
        else:
            self.button_right.set_button_image(paths["button_right"])
            self.button_right.resize(200)
            self.button_right.move(self.pos_x + 265, self.pos_y)

        self.button_left.update(screen)
        self.button_right.update(screen)

    def on_button_click(self, other_player):
        if self.button_left.check_click_no_state_change():
            self.change_current_image("down", other_player)
        elif self.button_right.check_click_no_state_change():
            self.change_current_image("up", other_player)


class CountriesSelection:
    def __init__(self):
        self.background = util.Image("backgroundfull3.png", 800, 450)
        self.player1_flag = Flag(1)
        self.player2_flag = Flag(2)
        self.country_names = load_flag_names()

        self.flag1_position = (375, 475)
        self.flag2_position = (1225, 475)

        self.player1_text = util.Text("Player 1", (350, 600), MAIN_FONT, color=(255, 255, 255), font_size=52)
        self.player1_text.set_position((self.flag1_position[0], self.flag1_position[1] - 200))
        self.player1_text.bold(True)
        self.player1_country_name = self.country_names[self.player1_flag.current_image]
        self.player1_country_name_text = util.Text(self.player1_country_name, (0, 0), MAIN_FONT, color=(255, 255, 255))
        self.player1_flag_background = util.Image(paths["flag_background"],
                                                  self.flag1_position[0], self.flag1_position[1])
        self.player1_flag_background.resize(55)
        self.player1_flag_background.move(self.flag1_position[0], self.flag1_position[1])

        self.player2_text = util.Text("Player 2", (350, 650), MAIN_FONT, color=(255, 255, 255), font_size=52)
        self.player2_text.set_position((self.flag2_position[0], self.flag2_position[1] - 200))
        self.player2_text.bold(True)
        self.player2_country_name = self.country_names[self.player2_flag.current_image]
        self.player2_country_name_text = util.Text(self.player2_country_name, (0, 0), MAIN_FONT, color=(255, 255, 255))
        self.player2_flag_background = util.Image(paths["flag_background"],
                                                  self.flag1_position[0], self.flag1_position[1])
        self.player2_flag_background.resize(55)
        self.player2_flag_background.move(self.flag2_position[0], self.flag2_position[1])

        self.back_button = util.Button(paths["back_button"], 800, 800, None)
        self.back_button.resize(150)
        self.back_button.move(950, 825)
        self.play_button = util.Button(paths["play_button"], 800, 800, None)
        self.play_button.resize(150)
        self.play_button.move(1375, 825)

    def update(self, screen, current_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player1_flag.on_button_click(self.player2_flag)
                self.player2_flag.on_button_click(self.player1_flag)
            if self.play_button.check_click(current_state, util.read_discipline(), event):
                util.save_country(self.player1_flag, 1)
                util.save_country(self.player2_flag, 2)
                self.loading_timer = TimingClock
                self.play_selected = True

            self.back_button.check_click(current_state, "single_discipline_menu", event)

        self.background.update(screen)

        self.player1_text.render(screen)
        self.player2_text.render(screen)
        self.player1_flag_background.update(screen)
        self.player2_flag_background.update(screen)
        self.player1_flag.update(screen)
        self.player2_flag.update(screen)

        self.player1_country_name = self.country_names[self.player1_flag.current_image]
        self.player1_country_name_text.set_text(self.player1_country_name)
        self.player1_country_name_text.set_position((self.flag1_position[0], self.flag1_position[1] + 200))
        self.player1_country_name_text.render(screen)

        self.player2_country_name = self.country_names[self.player2_flag.current_image]
        self.player2_country_name_text.set_text(self.player2_country_name)
        self.player2_country_name_text.set_position((self.flag2_position[0], self.flag2_position[1] + 200))
        self.player2_country_name_text.render(screen)

        if self.back_button.is_hovering():
            self.back_button.set_button_image(paths["back_button_active"])
            self.back_button.resize(150)
            self.back_button.move(1100, 825)
        else:
            self.back_button.set_button_image(paths["back_button"])
            self.back_button.resize(150)
            self.back_button.move(1100, 825)

        if self.play_button.is_hovering():
            self.play_button.set_button_image(paths["play_button_active"])
            self.play_button.resize(150)
            self.play_button.move(1425, 825)
        else:
            self.play_button.set_button_image(paths["play_button"])
            self.play_button.resize(150)
            self.play_button.move(1425, 825)

        self.back_button.update(screen)
        self.play_button.update(screen)

        pygame.display.flip()


