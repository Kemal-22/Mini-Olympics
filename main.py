import pygame
import util
import country
import game_running
import leaderboard
import game_jumping
import ctypes

pygame.init()
pygame.font.init()
ctypes.windll.user32.SetProcessDPIAware()

clock = pygame.time.Clock()
FPS = 60
WIDTH = 1600
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def test_func():
    #print("Working")
    pass


def test_func2():
    print("Working too")


class MainMenu:
    def __init__(self):
        self.main_menu_bg = util.Image("backgroundMainMenu.png", 800, 450)
        self.multiple_disciplines_button = util.Button("multipleDisciplinesButton.png", 800, 800, test_func)
        self.multiple_disciplines_button.resize(75)
        self.multiple_disciplines_button.move(800, 700)
        self.single_discipline_button = util.Button("singleDisciplineButton.png", 800, 500, None)
        self.single_discipline_button.resize(75)
        self.single_discipline_button.move(800, 525)
        self.main_menu_logo = util.Image("logo.png", 800, 100)
        self.main_menu_logo.resize(75)
        self.main_menu_logo.move(800, 250)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.main_menu_bg.update(screen)
        self.multiple_disciplines_button.check_click(current_state, "main_menu")
        self.multiple_disciplines_button.update(screen)
        if self.single_discipline_button.check_click(current_state, "single_discipline_menu"):
            return
        self.single_discipline_button.update(screen)
        self.main_menu_logo.update(screen)
        pygame.display.flip()


class SingleDisciplineMenu:
    def __init__(self):
        screen.fill((255, 255, 255))
        self.discipline_select_bg = util.Image("backgroundMainMenu.png", 800, 450)
        self.discipline_select_running200 = util.Button("running200selectbutton.png", 800, 300, test_func)
        self.discipline_select_jumping = util.Button("jumpingselectbutton.png", 800, 450, test_func)
        self.discipline_select_disc3 = util.Button("running200selectbutton.png", 800, 600, test_func)
        self.discipline_select_disc4 = util.Button("running200selectbutton.png", 800, 750, test_func)
        self.discipline_select_text = util.Image("select_a_discipline.png", 800, 110)
        self.back_button = util.Button("back_button.png", 800, 800, test_func)
        self.back_button.resize(47)
        self.back_button.move(1410, 835)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.discipline_select_bg.update(screen)
        self.discipline_select_text.update(screen)
        self.discipline_select_running200.update(screen)
        self.discipline_select_jumping.update(screen)
        self.discipline_select_disc3.update(screen)
        self.discipline_select_disc4.update(screen)
        self.back_button.update(screen)

        if self.discipline_select_running200.check_click(current_state, "countries"):
            util.save_discipline("running")
            util.read_discipline()

        elif self.discipline_select_jumping.check_click(current_state, "countries"):
            util.save_discipline("jumping")
            util.read_discipline()

        self.discipline_select_disc3.check_click(current_state, False)
        self.discipline_select_disc4.check_click(current_state, False)
        self.back_button.check_click(current_state, "main_menu")
        pygame.display.flip()


current_state = util.State()

running = True

player1_flag = country.Flag(1)
player2_flag = country.Flag(2)

initialization_checker = util.Initialized()
single_discipline_menu_obj = SingleDisciplineMenu()
main_menu_obj = MainMenu()

game = None
leaderboard_obj = None

while running:
    if current_state.state == "main_menu":
        main_menu_obj.update()
    if current_state.state == "single_discipline_menu":
        single_discipline_menu_obj.update()
    if current_state.state == "countries":
        country.countries_select(screen, current_state, player1_flag, player2_flag)

    if current_state.state == "running":
        if game is None:
            game = game_running.Game()
            leaderboard_obj = None
        else:
            game.run_game(screen, current_state)

    if current_state.state == "leaderboard":
        if leaderboard_obj is None:
            leaderboard_obj = leaderboard.Leaderboard(current_state)
            game = None
        else:
            leaderboard_obj.run_leaderboard(screen, current_state)

    if current_state.state == "jumping":
        if game is None:
            game = game_jumping.Game()
            leaderboard_obj = None
        else:
            game.run_game(screen)

    clock.tick(FPS)

pygame.quit()
