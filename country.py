import pygame
import util


def load_flag_list():
    list_file = open("flag_list.txt", "r")
    countries_array = []
    for i in list_file:
        word = i.replace('\n', '')
        countries_array.append(word)

    return countries_array


def blank():
    pass


def load_discipline():
    pass



def load_flag_images():
    countries_array = load_flag_list()
    countries_images_array = []
    for country in countries_array:
        flag = util.Image("./flags/" + country + ".png", 100, 100)
        countries_images_array.append(flag)

    return countries_images_array


class Flag:

    def __init__(self, id):
        self.name_list = load_flag_list()
        self.images = load_flag_images()
        self.currentimage = 0
        if id == 1:
            for country in self.images:
                self.pos_x = 335
                self.pos_y = 400
                country.resize(50)
                country.move(self.pos_x, self.pos_y)

        else:
            for country in self.images:
                self.pos_x = 1250
                self.pos_y = 400
                country.resize(50)
                country.move(self.pos_x, self.pos_y)
                self.currentimage = 1

        self.currentimageobject = self.images[0]
        self.id = id

        self.button_left = util.Button("button_triangle_left.png", self.pos_x - 50, self.pos_y, self.test_function())
        self.button_left.resize(30)
        self.button_left.move(self.pos_x - 265, self.pos_y)

        self.button_right = util.Button("button_triangle_right.png", self.pos_x - 50, self.pos_y, self.test_function())
        self.button_right.resize(30)
        self.button_right.move(self.pos_x + 265, self.pos_y)


    def test_function(self):
        print("working")


    def change_current_image(self, dir, other_player):
        if dir == "up" and self.currentimage + 1 < len(self.name_list):
            if other_player.currentimage != self.currentimage + 1:
                self.currentimage += 1
            elif other_player.currentimage == self.currentimage + 1 and self.currentimage + 2 < len(self.name_list):
                self.currentimage += 2
            else:
                self.currentimage = 0

        elif dir == "up" and self.currentimage + 1 >= len(self.name_list):
            if other_player.currentimage == 0:
                self.currentimage = 1
            else:
                self.currentimage = 0

        elif dir == "down" and self.currentimage - 1 >= 0:
            if other_player.currentimage != self.currentimage - 1:
                self.currentimage -= 1
            elif other_player.currentimage == self.currentimage - 1 and self.currentimage - 2 >= 0:
                self.currentimage -= 2
            else:
                self.currentimage = len(self.name_list) - 1

        elif dir == "down" and self.currentimage - 1 <= 0:
            if other_player.currentimage == len(self.name_list) - 1:
                self.currentimage = len(self.name_list) - 2
            else:
                self.currentimage = len(self.name_list) - 1

    def update_image(self, screen):
        self.currentimageobject = self.images[self.currentimage]
        self.currentimageobject.update(screen)
        self.button_left.update(screen)
        self.button_right.update(screen)


    def on_button_click(self, other_player):
        if self.button_left.check_click_no_state_change():
            self.change_current_image("down", other_player)
        elif self.button_right.check_click_no_state_change():
            self.change_current_image("up", other_player)


def countries_select(screen, current_state, player1, player2):
    if current_state.state == "countries":
        init = True
        if init:
            background = util.Image("backgroundMainMenu.png", 800, 450)
            player1_text = util.Image("player_1_text.png", 400, 100)
            player1_text.resize(80)
            player1_text.move(350, 650)
            player2_text = util.Image("player_2_text.png", 1200, 100)
            player2_text.resize(80)
            player2_text.move(1250, 650)
            select_text = util.Image("select_your_country.png", 800, 110)
            back_button = util.Button("back_button.png", 800, 800, blank)
            back_button.resize(50)
            back_button.move(950, 825)
            play_button = util.Button("play_button.png", 800, 800, blank)
            play_button.resize(50)
            play_button.move(1375, 825)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player1.on_button_click(player2)
                player2.on_button_click(player1)

        background.update(screen)

        player1_text.update(screen)
        player2_text.update(screen)
        select_text.update(screen)
        player1.update_image(screen)
        player2.update_image(screen)
        back_button.update(screen)
        if back_button.check_click(current_state, "single_discipline_menu"):
            player1.currentimage = 0
            player2.currentimage = 1

        play_button.update(screen)
        if play_button.check_click(current_state, util.read_discipline()):
            util.save_country(player1, 1)
            util.save_country(player2, 2)


        pygame.display.flip()

