import pygame
import util
import math


MAIN_FONT = "./font/PublicPixel-0W6DP.ttf"


class Player(pygame.sprite.Sprite):
    def __init__(self, id):
        pygame.sprite.Sprite.__init__(self)
        defaultxpos = 800
        defaultypos = 750
        self.finished = False
        self.slowdown = 0.14
        self.acceleration = 1
        self.max_speed = 15
        self.started = False
        self.speed = 0
        self.country = util.load_country(id)
        print(self.country)
        self.in_front = None
        self.time = None

        self.sprites = []
        self.sprites.append(pygame.image.load("./characters/" + self.country + "/0.png"))
        self.sprites.append(pygame.image.load("./characters/" + self.country + "/1.png"))
        self.sprites.append(pygame.image.load("./characters/" + self.country + "/2.png"))
        self.sprites.append(pygame.image.load("./characters/" + self.country + "/3.png"))
        self.sprites.append(pygame.image.load("./characters/" + self.country + "/4.png"))
        self.current_sprite = 0
        self.scale = 0.5

        for i in range(0, len(self.sprites)):
            width = self.sprites[i].get_width()
            height = self.sprites[i].get_height()
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (round(width * self.scale), round(height * self.scale)))

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [defaultxpos, 675]

        self.since_last_change = 1
        self.last_change = 0

    def get_slowdown(self):
        slowdown = ((self.speed / 0.95) / 100)
        return slowdown

    def update(self, screen, player2, line):

        print("Speed is: " + str(round(self.speed, 2)) + " and slowdown is: " + str(round(self.slowdown, 2)))
        self.slowdown = self.get_slowdown()

        if self.rect.right > line.rect.left:
            self.finished = True

        if self.finished is True:
            if self.speed > 0:
                self.speed -= self.slowdown * 3
            else:
                self.speed = 0

        elif self.speed - self.slowdown < 0:
            self.speed = 0
        else:
            self.speed -= self.slowdown

        self.since_last_change = (pygame.time.get_ticks() - self.last_change) / 1000
        if self.speed == 0:
            self.current_sprite = 0

        elif self.since_last_change > (-0.01 * self.speed + 0.25):
            if self.current_sprite + 1 < len(self.sprites):
                self.current_sprite += 1
                self.last_change = pygame.time.get_ticks()
            else:
                self.current_sprite = 1
                self.last_change = pygame.time.get_ticks()

        self.image = self.sprites[self.current_sprite]
        screen.blit(self.image, self.rect)

    def run_clicked(self):
        if self.speed + self.acceleration <= self.max_speed:
            self.speed += self.acceleration
        else:
            self.speed = self.max_speed


class TimingClock:
    def __init__(self):
        self.start = pygame.time.get_ticks()

    def get_current_time_in_miliseconds(self):
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

    def update(self, screen, time):
        self.image.update(screen)
        time = str(time)
        self.text.set_text(time)
        self.text.render(screen)


class Game:
    def __init__(self):
        self.background = util.Image("background20k.png", 800, 450)
        self.background.rect.left = 0
        self.pixels_per_meter = 90
        self.finish_line = util.Image("finish_line.png", 8500, 853)
        self.finish_line.rect.left = 10 * self.pixels_per_meter + 800
        self.finish_line.rect.bottom = 900
        self.finish_line_spawned = False
        self.count3 = util.Image("count_3.png", 0, 0)
        self.count3.resize(50)
        self.count3.move(800, 450)
        self.count2 = util.Image("count_2.png", 0, 0)
        self.count2.resize(50)
        self.count2.move(800, 450)
        self.count1 = util.Image("count_1.png", 0, 0)
        self.count1.resize(50)
        self.count1.move(800, 450)
        self.false_start = util.Image("false_start.png", 800, 450)
        self.false_start.resize(25)
        self.false_start.move(800, 450)
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

        self.false_start_happened = False
        self.player1_text = util.Image("player_1_text.png", 400, 100)
        self.player1_text.resize(80)
        self.player1_text.move(800, 325)
        self.player2_text = util.Image("player_2_text.png", 1200, 100)
        self.player2_text.resize(80)
        self.player2_text.move(800, 325)
        self.winner_text = util.Image("winner.png", 800, 350)
        self.winner_text.resize(30)
        self.winner_text.move(800, 350)
        self.end_start_timer = 0
        self.end_timer = 0
        self.game_timer_widget = TimerWidget()

    def check_for_false_start(self):
        if not self.running_started:
            if self.player1.started is True:
                return self.player1
            elif self.player2.started is True:
                return self.player2
            else:
                return False

    def false_start_logic(self):
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
            self.false_start.update(screen)
            if self.winner == self.player1:
                self.player2_text.update(screen)
            elif self.winner == self.player2:
                self.player1_text.update(screen)

    def display_winner(self, screen):
        if self.winner is not None and self.false_start_happened is not True:
            self.player1_text.move(800, 475)
            self.player2_text.move(800, 475)
            if self.winner == self.player1:
                self.winner_text.update(screen)
                self.player1_text.update(screen)
            else:
                self.winner_text.update(screen)
                self.player2_text.update(screen)

    def measure_distance(self, background):
        distance = abs(background.rect.left) / 90
        return distance

    def move_background(self, background, player1, player2):
        if player1.rect.centerx == 800:
            background.rect.x -= player1.speed
        elif player2.rect.centerx == 800:
            background.rect.x -= player2.speed

        if background.rect.right < 0:
            background.rect.left = 1595

    def move_finish_line(self, finish_line):
        finish_line.rect.left = ((100 - self.measure_distance(self.background)) * 90) + 800

    def check_for_winner(self, player1, player2):
        if player1.finished is True and player2.finished is False:
            self.winner = self.player1

        elif player2.finished is True and player1.finished is False:
            self.winner = self.player2

        return False

    def player_movement(self, player1, player2):
        if player1.rect.centerx > 800:
            player1.rect.centerx = 800
        if player2.rect.centerx > 800:
            player2.rect.centerx = 800

        if player1.rect.centerx == 800 and player2.rect.centerx == 800:
            if player1.speed < player2.speed:
                player1.rect.centerx -= player2.speed - player1.speed
            elif player1.speed > player2.speed:
                player2.rect.centerx -= player1.speed - player2.speed
        elif player1.rect.centerx < 800 and player2.rect.centerx == 800:
            if player1.speed < player2.speed:
                player1.rect.centerx -= player2.speed - player1.speed
            elif player1.speed > player2.speed:
                player1.rect.centerx += player1.speed - player2.speed
        elif player2.rect.centerx < 800 and player1.rect.centerx == 800:
            if player2.speed < player1.speed:
                player2.rect.centerx -= player1.speed - player2.speed
            elif player2.speed > player1.speed:
                player2.rect.centerx += player2.speed - player1.speed

    def run_timing_logic(self, screen):
        if self.running_started is False:
            if self.before_start_timer.get_current_time_in_seconds() == 3:
                self.running_started = True
                self.running_timer = TimingClock()

            elif self.before_start_timer.get_current_time_in_seconds() == 2 and self.false_start_happened is False:
                self.count1.update(screen)

            elif self.before_start_timer.get_current_time_in_seconds() == 1 and self.false_start_happened is False:
                self.count2.update(screen)

            elif self.before_start_timer.get_current_time_in_seconds() == 0 and self.false_start_happened is False:
                self.count3.update(screen)

        elif self.running_started is True and self.false_start_happened is True:
            self.running_timer = "F.S."

        else:
            self.game_timer_widget.update(screen, str(self.running_timer.get_current_time_in_miliseconds()))

        if self.winner is self.player1 and self.player1.time is None:
            self.player1.time = self.running_timer.get_current_time_in_seconds()

        elif self.winner is self.player2 and self.player2.time is None:
            self.player2.time = self.running_timer.get_current_time_in_seconds()

        elif self.winner is self.player1 and self.player2.finished is True and self.player2.time is None:
            self.player2.time = self.running_timer.get_current_time_in_seconds()

        elif self.winner is self.player2 and self.player1.finished is True and self.player1.time is None:
            self.player1.time = self.running_timer.get_current_time_in_seconds()

    def end_timing(self):
        if self.winner is not None and self.end_start_timer is 0:
            self.end_start_timer = pygame.time.get_ticks()
        elif self.winner is not None and self.end_start_timer is not 0:
            self.end_timer = math.floor((pygame.time.get_ticks() - self.end_start_timer) / 1000)

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
                        self.player1.speed = self.player1.max_speed - self.player1.max_speed * 0.3
                    else:
                        if self.player1.finished is False:
                            self.player1.run_clicked()

                if event.key == pygame.K_i:
                    if not self.player2.started:
                        self.player2.started = True
                        self.player2.speed = self.player2.max_speed - self.player2.max_speed * 0.3
                    else:
                        if self.player2.finished is False:
                            self.player2.run_clicked()

        self.move_background(self.background, self.player1, self.player2)
        self.move_finish_line(self.finish_line)
        self.player_movement(self.player1, self.player2)
        self.background.update(screen)
        self.finish_line.update(screen)
        self.player1.update(screen, self.player2, self.finish_line)
        self.player2.update(screen, self.player1, self.finish_line)

        self.false_start_logic()
        self.false_start_display(screen)
        self.run_timing_logic(screen)
        self.end_timing()
        if self.end_timer == 3:
            current_state.state = "leaderboard"
            current_state.prev_state = "running"

        self.display_winner(screen)

        if self.winner is None:
            self.check_for_winner(self.player1, self.player2)
        else:
            self.record_data()

        pygame.display.flip()
