import pygame
import util


WHITE = (255, 255, 255)
MAIN_FONT = "./Assets/fonts/PublicPixel-0W6DP.ttf"


def load_highscore():
    f = open("highscore.txt", "r")
    highscore = f.read()
    print(highscore)
    f.close()
    return highscore


def record_highscore(winning_time):
    f = open("highscore.txt", "w")
    f.write(winning_time)
    f.close()


def load_winner():
    f = open("winner_and_time.txt", "r")
    lines = f.readlines()
    temp = lines[0]
    winner = temp.replace('\n', '')
    print(winner)
    return winner


def get_player_time(player):
    f = open("winner_and_time.txt", 'r')
    lines = f.readlines()

    if player == 1:
        temp = lines[1]
    else:
        temp = lines[2]

    time = temp.replace('\n', '')
    if time == "None":
        time = "DNF"

    return time


def get_text_pos(text_surface, base, place):
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    base_slot_height = base.get_image_height() / 3
    base_top = base.rect.top
    base_left = base.rect.left
    base_right = base.rect.right
    box_left = round((base.get_image_width() / 100) * 73.812) + base_left
    box_center = box_left + ((base_right - box_left) / 2)
    slot1_center = (base_top + (2 * base_slot_height)) - (base_slot_height / 2)
    slot2_center = (base_top + (3 * base_slot_height)) - (base_slot_height / 2)
    text_left = box_center - (text_width / 2)

    if place == 1:
        position_x = text_left
        position_y = slot1_center - (text_height / 2)
        position = (position_x, position_y)
        return position

    else:
        position_x = text_left
        position_y = slot2_center - (text_height / 2)
        position = (position_x, position_y)
        return position


def winner_and_hs_text_pos(base, text_surface, id):
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    base_slot_height = base.get_image_height() / 2
    base_top = base.rect.top
    base_left = base.rect.left
    base_right = base.rect.right
    slot_centerx = base_right - ((base_right - base_left) / 4)
    if id == 1:
        print("Didnt get that far")
        slot_centery = base_top + (base_slot_height / 2)
        positionx = slot_centerx - (text_width / 2)
        positiony = slot_centery - (text_height / 2)
        position = (positionx, positiony)
        return position
    else:
        print("Got this far")
        slot_centery = base_top + ((base_slot_height / 2) + base_slot_height)
        positionx = slot_centerx - (text_width / 2)
        positiony = slot_centery - (text_height / 2)
        position = (positionx, positiony)
        return position


class PlayerFlag:
    def __init__(self, player, place, base_image):
        if player == 1:
            f = open("player1_flag.txt", "r")
            temp = f.read()
            word = temp.replace('\n', '')
            self.flag_name = word
            f.close()
            self.image = util.Image("./flags/" + self.flag_name + ".png", 100, 100)
        else:
            f = open("player2_flag.txt", "r")
            temp = f.read()
            word = temp.replace('\n', '')
            self.flag_name = word
            f.close()
            self.image = util.Image("./flags/" + self.flag_name + ".png", 100, 100)

        if place == 1:

            width = (base_image.get_image_width() / 100) * 18.75
            self.image.set_width(width)
            self.image.rect.left = base_image.rect.left
            self.image.rect.top = base_image.rect.top + base_image.get_image_height() / 3
        else:

            width = (base_image.get_image_width() / 100) * 18.75
            self.image.set_width(width)
            self.image.rect.left = base_image.rect.left
            self.image.rect.top = base_image.rect.top + base_image.get_image_height() / 1.5

    def display_flag(self, screen):
        self.image.update(screen)


class Leaderboard:
    def __init__(self, current_state):
        # Next state could be loaded from a file containing the list of disciplines when multi disciplines are implemented. If it is equal to one, then the next state is the main menu
        self.next_state = "main_menu"
        self.winner = load_winner()
        self.highscore = load_highscore()

        self.highscore_text = util.Text(self.highscore, (100, 200), MAIN_FONT, font_size=50, color=WHITE)
        self.previous_state = current_state.prev_state
        self.background = util.Image("backgroundMainMenu.png", 800, 450)
        self.background.rect.left = 0
        if self.winner == "player1":
            self.base = util.Image("leaderboard_base1.png", 0, 0)
            self.player1_time = get_player_time(1)
            self.player2_time = get_player_time(2)
            self.winner_text = util.Text(self.player1_time, (100, 300), MAIN_FONT, font_size=50, color=WHITE)
            self.winning_time = self.player1_time

        else:
            self.base = util.Image("leaderboard_base2.png", 0, 0)
            self.player1_time = get_player_time(2)
            self.player2_time = get_player_time(1)
            self.winner_text = util.Text(self.player2_time, (100, 300), MAIN_FONT, font_size=50, color=WHITE)
            self.winning_time = self.player2_time

        self.base.resize(70)
        self.base_position = (800, 250)
        self.base.move(self.base_position[0], self.base_position[1])
        self.highscore_base = util.Image("highscore_base.png", 0, 0)
        self.highscore_base.resize(50)
        self.highscore_base_position_x = self.base.rect.left + (self.highscore_base.get_image_width() / 2)
        self.highscore_base_position_y = self.base.rect.bottom + 125
        self.highscore_base.move(self.highscore_base_position_x, self.highscore_base_position_y)
        self.highscore_text.set_position(winner_and_hs_text_pos(self.highscore_base, self.highscore_text.text_surface, 1))
        self.new_highscore = util.Image("new_highscore.png", (self.highscore_base.rect.right + 350), (self.highscore_base.rect.top + (self.highscore_base.get_image_height() / 2)))
        self.winner_text.set_position(winner_and_hs_text_pos(self.highscore_base, self.winner_text.text_surface, 2))

        if self.winner == "player1":
            self.player1_flag = PlayerFlag(1, 1, self.base)
            self.player2_flag = PlayerFlag(2, 2, self.base)
        else:
            self.player1_flag = PlayerFlag(2, 1, self.base)
            self.player2_flag = PlayerFlag(1, 2, self.base)

        self.font_size = 65

        self.player1_time_text = util.Text(self.player1_time, (100, 200), MAIN_FONT, font_size=self.font_size, color=WHITE)
        self.player2_time_text = util.Text(self.player2_time, (100, 300), MAIN_FONT, font_size=self.font_size, color=WHITE)
        print("Player 1 Time: " + self.player1_time)
        print("Player 2 Time: " + self.player2_time)

        if self.winner == "player1":
            self.player1_time_text_pos = get_text_pos(self.player1_time_text.text_surface, self.base, 1)
            self.player1_time_text.set_position(self.player1_time_text_pos)
            self.player2_time_text_pos = get_text_pos(self.player2_time_text.text_surface, self.base, 2)
            self.player2_time_text.set_position(self.player2_time_text_pos)

        else:

            self.player1_time_text_pos = get_text_pos(self.player1_time_text.text_surface, self.base, 2)
            self.player1_time_text.set_position(self.player1_time_text_pos)
            self.player2_time_text_pos = get_text_pos(self.player2_time_text.text_surface, self.base, 1)
            self.player2_time_text.set_position(self.player2_time_text_pos)

        self.restart_button_pos = (1000, 825)
        self.next_button_pos = (self.restart_button_pos[0] + 400, self.restart_button_pos[1])
        self.next_button = util.Button("next_button.png", 100, 100, None)
        self.next_button.resize(50)
        self.next_button.move(self.next_button_pos[0], self.next_button_pos[1])
        self.restart_button = util.Button("restart_button.png", 100, 100, None)
        self.restart_button.resize(50)
        self.restart_button.move(self.restart_button_pos[0], self.restart_button_pos[1])

        print(self.winning_time)
        print(self.highscore)
        if self.winning_time < self.highscore:
            print("Got here")
            record_highscore(self.winning_time)

    def run_leaderboard(self, screen, current_state):

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_button.check_click_no_state_change():
                    current_state.state = self.next_state
                if self.restart_button.check_click_no_state_change():
                    current_state.state = self.previous_state

        self.background.update(screen)
        self.base.update(screen)
        self.highscore_base.update(screen)
        self.highscore_text.render(screen)
        self.winner_text.render(screen)
        self.next_button.update(screen)
        self.restart_button.update(screen)
        self.player1_flag.display_flag(screen)
        self.player2_flag.display_flag(screen)
        self.player1_time_text.render(screen)
        self.player2_time_text.render(screen)
        if self.winning_time < self.highscore:
            self.new_highscore.update(screen)

        pygame.display.flip()
