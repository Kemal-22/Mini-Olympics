import pygame
import util
import math


MAIN_FONT = "./font/PublicPixel-0W6DP.ttf"


class Player(pygame.sprite.Sprite):
    def __init__(self, player_number):
        pygame.sprite.Sprite.__init__(self)
        defaultxpos = 800
        if player_number == 1:
            defaultypos = 600
        else:
            defaultypos = 660
        self.finished = False
        self.current_slowdown = 0.14  # Default 0.14 Doesnt work anymore
        self.acceleration = 2  # Default 1
        self.max_speed = 20
        self.started = False
        self.speed = 0
        self.country = util.load_country(player_number)
        self.is_in_front = None
        self.time = None
        self.playernum = player_number

        self.animation_states = []
        self.current_animation_state = 0
        self.sprite_size_scale = 0.6   # Scales the players size on screen
        # Load all animation states and scale them according to sprite scale
        for animation_state in range(0, 7):
            temp_sprite = pygame.image.load("./characters/" + self.country + "/" + str(animation_state) + ".png")
            temp_sprite_width = temp_sprite.get_width()
            temp_sprite_height = temp_sprite.get_height()
            temp_sprite = pygame.transform.scale(temp_sprite, (round(temp_sprite_width * self.sprite_size_scale),
                                                               round(temp_sprite_height * self.sprite_size_scale)))
            self.animation_states.append(temp_sprite)

        self.current_sprite = self.animation_states[0]
        self.current_sprite_rect = self.current_sprite.get_rect()
        self.current_sprite_rect.center = [defaultxpos, defaultypos]

        self.animation_timer = TimingClock()
        self.time_since_last_animation_change = 0
        self.last_animation_change = 0

    def get_slowdown(self):
        #slowdown = ((self.speed / 0.95) / 100)
        slowdown = 0.02 * pow(1.2, self.speed)
        return slowdown

    def check_if_finished(self, line):
        if self.current_sprite_rect.right > line.rect.left:
            self.finished = True

    def slow_player_down(self):
        self.current_slowdown = self.get_slowdown()

        if self.finished is True:
            if self.speed >= 1:  # This is set to 1 because values less than this do not move the player, and the
                # slowdown will never reach 0
                self.speed -= self.current_slowdown * 3
            else:
                self.speed = 0

        elif self.speed - self.current_slowdown < 1:
            self.speed = 0

        else:
            self.speed -= self.current_slowdown

    def change_animation_state(self):
        self.time_since_last_animation_change = (self.animation_timer.get_current_time_in_milliseconds()
                                                 - self.last_animation_change) / 1000
        animation_change_interval = (-0.01 * self.speed + 0.20)

        if self.speed <= 1:
            self.current_animation_state = 0

        elif self.time_since_last_animation_change > animation_change_interval:

            if self.current_animation_state + 1 < len(self.animation_states):
                self.current_animation_state += 1
            else:
                self.current_animation_state = 1

            self.last_animation_change = self.animation_timer.get_current_time_in_milliseconds()

    def update_player(self, screen, line):
        self.check_if_finished(line)
        self.slow_player_down()
        self.change_animation_state()

        self.current_sprite = self.animation_states[self.current_animation_state]
        screen.blit(self.current_sprite, self.current_sprite_rect)

    def on_run_keybind(self):
        if self.speed + self.acceleration <= self.max_speed:
            self.speed += self.acceleration
        else:
            self.speed = self.max_speed


class TimingClock:
    def __init__(self):
        self.start = pygame.time.get_ticks()

    def get_current_time_in_milliseconds(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.start

    def get_current_time_in_seconds(self):
        current_time = pygame.time.get_ticks()
        return math.floor((current_time - self.start) / 1000)


class TimerWidget:
    def __init__(self):
        self.image_pos_x = 1400
        self.image_pos_y = 800
        self.image = util.Image("time_image.png", self.image_pos_x, self.image_pos_y)
        self.image.resize(30)
        self.image.move(self.image_pos_x, self.image_pos_y)

        self.text_y_position = self.image_pos_y + self.image.get_image_height() / 4
        self.text_x_position = self.image_pos_x
        self.text = util.Text("0.00", (self.text_x_position, self.text_y_position), MAIN_FONT, font_size=35,
                              color=(255, 255, 255))
        self.time = 0

    def update(self, screen, time=None):
        self.image.update(screen)
        if time is not None:
            self.text.set_text(str(time))
        self.text.render(screen)


class Game:
    def __init__(self):
        self.background = util.Image("background20k1.png", 800, 450)
        self.background.rect.left = 0
        self.pixels_per_meter = 90
        self.finish_line = util.Image("finish_line.png", 8500, 853)
        self.finish_line.rect.left = 10 * self.pixels_per_meter + 800
        self.finish_line.rect.bottom = 900
        self.finish_line_spawned = False

        self.start_countdown_number_3 = util.Image("count_3.png", 0, 0)
        self.start_countdown_number_2 = util.Image("count_2.png", 0, 0)
        self.start_countdown_number_1 = util.Image("count_1.png", 0, 0)
        self.false_start_image = util.Image("false_start.png", 800, 450)

        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player1.speed = 0
        self.player2.speed = 0
        self.players = pygame.sprite.Group()
        self.players.add(self.player1)
        self.players.add(self.player2)
        self.winner = None

        self.running_started = False
        self.before_start_timer = TimingClock()
        self.running_timer = None
        self.finish_time = None
        self.end_timer = None
        self.game_timer_widget = TimerWidget()
        self.false_start_happened = False

        self.player1_text = util.Image("player_1_text.png", 400, 100)
        self.player2_text = util.Image("player_2_text.png", 1200, 100)
        self.winner_text = util.Image("winner.png", 800, 350)

        self.resize_and_place_images()

    def resize_and_place_images(self):
        self.start_countdown_number_3.resize(50)
        self.start_countdown_number_3.move(800, 450)
        self.start_countdown_number_2.resize(50)
        self.start_countdown_number_2.move(800, 450)
        self.start_countdown_number_1.resize(50)
        self.start_countdown_number_1.move(800, 450)
        self.false_start_image.resize(25)
        self.false_start_image.move(800, 450)

        self.player1_text.resize(80)
        self.player1_text.move(800, 325)
        self.player2_text.resize(80)
        self.player2_text.move(800, 325)
        self.winner_text.resize(30)
        self.winner_text.move(800, 350)

    def check_for_false_start(self):
        if not self.running_started:
            if self.player1.started is True:
                return self.player1
            elif self.player2.started is True:
                return self.player2
            else:
                return False

    def false_start_logic(self):
        if self.winner is not None:
            return False
        if self.check_for_false_start() == self.player1:
            self.winner = self.player2
            self.player1.finished = True
            self.player2.finished = True
            self.false_start_happened = True
        elif self.check_for_false_start() == self.player2:
            self.winner = self.player1
            self.player1.finished = True
            self.player2.finished = True
            self.false_start_happened = True

    def false_start_display(self, screen):
        if self.false_start_happened:
            self.false_start_image.update(screen)
            if self.winner == self.player1:
                self.player2_text.update(screen)
            elif self.winner == self.player2:
                self.player1_text.update(screen)

    def display_winner(self, screen):
        if self.winner is None or self.false_start_happened:
            return False

        if self.winner == self.player1:
            self.player1_text.move(800, 475)
            self.winner_text.update(screen)
            self.player1_text.update(screen)
        else:
            self.player2_text.move(800, 475)
            self.winner_text.update(screen)
            self.player2_text.update(screen)

    @staticmethod
    def measure_distance(background):
        distance = abs(background.rect.left) / 90
        return distance

    def move_background(self):
        if self.player1.is_in_front:
            self.background.rect.x -= self.player1.speed
        elif self.player2.is_in_front:
            self.background.rect.x -= self.player2.speed

    def move_finish_line(self, finish_line):
        finish_line.rect.left = ((100 - self.measure_distance(self.background)) * 90) + 800

    def check_for_winner(self, player1, player2):
        if player1.finished is True and player2.finished is False:
            self.winner = self.player1

        elif player2.finished is True and player1.finished is False:
            self.winner = self.player2

        return False

    def player_movement(self):
        if self.player1.current_sprite_rect.centerx > 800:
            self.player1.current_sprite_rect.centerx = 800
        if self.player2.current_sprite_rect.centerx > 800:
            self.player2.current_sprite_rect.centerx = 800
        # This part of the code keeps the player in front in the center of the screen while moving the second player
        # forwards or backwards. Also keeps track of who is in front.

        if self.player1.current_sprite_rect.centerx == 800 and self.player2.current_sprite_rect.centerx == 800:

            if self.player1.speed < self.player2.speed:
                self.player1.current_sprite_rect.centerx -= self.player2.speed - self.player1.speed
                self.player2.is_in_front = True
                self.player1.is_in_front = False
            elif self.player1.speed >= self.player2.speed:
                self.player2.current_sprite_rect.centerx -= self.player1.speed - self.player2.speed
                self.player2.is_in_front = False
                self.player1.is_in_front = True

        elif self.player1.current_sprite_rect.centerx < 800 and self.player2.current_sprite_rect.centerx == 800:
            self.player1.is_in_front = False
            self.player2.is_in_front = True
            if self.player1.speed < self.player2.speed:
                self.player1.current_sprite_rect.centerx -= self.player2.speed - self.player1.speed
            elif self.player1.speed > self.player2.speed:
                self.player1.current_sprite_rect.centerx += self.player1.speed - self.player2.speed

        elif self.player2.current_sprite_rect.centerx < 800 and self.player1.current_sprite_rect.centerx == 800:
            self.player1.is_in_front = True
            self.player2.is_in_front = False
            if self.player2.speed < self.player1.speed:
                self.player2.current_sprite_rect.centerx -= self.player1.speed - self.player2.speed
            elif self.player2.speed > self.player1.speed:
                self.player2.current_sprite_rect.centerx += self.player2.speed - self.player1.speed

    def running_start_countdown_timer(self, screen):
        if self.running_started or self.false_start_happened:
            return False

        if self.before_start_timer.get_current_time_in_seconds() == 3:
            self.running_started = True
            self.running_timer = TimingClock()

        elif self.before_start_timer.get_current_time_in_seconds() == 2:
            self.start_countdown_number_1.update(screen)

        elif self.before_start_timer.get_current_time_in_seconds() == 1:
            self.start_countdown_number_2.update(screen)

        elif self.before_start_timer.get_current_time_in_seconds() == 0:
            self.start_countdown_number_3.update(screen)

    def before_leaderboard_timer(self, current_state):
        if self.end_timer is None:
            if self.winner is not None:
                self.end_timer = TimingClock()
            return True

        if self.end_timer.get_current_time_in_seconds() >= 3:
            current_state.state = "leaderboard"
            current_state.prev_state = "running"
            return True

    def main_running_timer(self, screen):
        if not self.running_started:
            return False

        if self.winner is None:
            time = str(round(self.running_timer.get_current_time_in_milliseconds() / 1000, 1))
            self.game_timer_widget.update(screen, time)
        else:
            self.game_timer_widget.update(screen)

    def record_timings(self):
        if not self.running_started:
            return False

        current_time = round(self.running_timer.get_current_time_in_milliseconds() / 1000, 1)

        if self.player1.finished and self.player1.time is None:
            self.player1.time = current_time

        elif self.player2.finished and self.player2.time is None:
            self.player2.time = current_time

    def false_start_timing(self):
        if self.false_start_happened:
            self.running_timer = "F.S."
            self.player1.time = "F.S."
            self.player2.time = "F.S."

    def run_timing_logic(self, screen, current_state):
        self.running_start_countdown_timer(screen)
        self.main_running_timer(screen)
        self.record_timings()
        self.false_start_timing()
        self.before_leaderboard_timer(current_state)

    def record_data(self):
        f = open("winner_and_time.txt", "w")
        if self.winner == self.player1:
            f.write("player1\n")
        else:
            f.write("player2\n")

        if self.winner == self.player1:
            f.write(str(self.player1.time) + "\n")
            f.write(str(self.player2.time) + "\n")
        else:
            f.write(str(self.player2.time) + "\n")
            f.write(str(self.player1.time) + "\n")

    def run_game(self, screen, current_state):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if not self.player1.started:
                        self.player1.started = True
                        # Players start at 70% of max speed
                        self.player1.speed = self.player1.max_speed - self.player1.max_speed * 0.3
                    else:
                        if self.player1.finished is False:
                            self.player1.on_run_keybind()

                if event.key == pygame.K_i:
                    if not self.player2.started:
                        self.player2.started = True
                        self.player2.speed = self.player2.max_speed - self.player2.max_speed * 0.3
                    else:
                        if self.player2.finished is False:
                            self.player2.on_run_keybind()

        self.move_background()
        self.move_finish_line(self.finish_line)
        self.player_movement()

        self.background.update(screen)
        self.finish_line.update(screen)
        self.player1.update_player(screen, self.finish_line)
        self.player2.update_player(screen, self.finish_line)

        self.false_start_logic()
        self.false_start_display(screen)
        self.run_timing_logic(screen, current_state)
        self.display_winner(screen)

        if self.winner is None:
            self.check_for_winner(self.player1, self.player2)
        else:
            self.record_data()

        pygame.display.flip()
