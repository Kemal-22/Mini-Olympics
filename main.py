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

current_state = util.State()


def test_func():
    #print("Working")
    pass


def test_func2():
    print("Working too")


def main_menu():
    if current_state.state == "main_menu":
        init = True

        if init:
            main_menu_bg = util.Image("backgroundMainMenu.png", 800, 450)
            multiple_disciplines_button = util.Button("multipleDisciplinesButton.png", 800, 800, test_func)
            multiple_disciplines_button.resize(75)
            multiple_disciplines_button.move(800, 700)
            single_discipline_button = util.Button("singleDisciplineButton.png", 800, 500, single_discipline_menu)
            single_discipline_button.resize(75)
            single_discipline_button.move(800, 525)
            main_menu_logo = util.Image("logo.png", 800, 100)
            main_menu_logo.resize(75)
            main_menu_logo.move(800, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        main_menu_bg.update(screen)
        multiple_disciplines_button.check_click(current_state, "main_menu")
        multiple_disciplines_button.update(screen)
        if single_discipline_button.check_click(current_state, "single_discipline_menu"):
            return
        single_discipline_button.update(screen)
        main_menu_logo.update(screen)
        pygame.display.flip()


def single_discipline_menu():
    if current_state.state == "single_discipline_menu":
        init = True
        if init:
            screen.fill((255, 255, 255))
            discipline_select_bg = util.Image("backgroundMainMenu.png", 800, 450)
            discipline_select_running200 = util.Button("running200selectbutton.png", 800, 300, test_func)
            discipline_select_jumping = util.Button("jumpingselectbutton.png", 800, 450, test_func)
            discipline_select_disc3 = util.Button("running200selectbutton.png", 800, 600, test_func)
            discipline_select_disc4 = util.Button("running200selectbutton.png", 800, 750, test_func)
            discipline_select_text = util.Image("select_a_discipline.png", 800, 110)
            back_button = util.Button("back_button.png", 800, 800, test_func)
            back_button.resize(47)
            back_button.move(1410, 835)
            init = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        discipline_select_bg.update(screen)
        discipline_select_text.update(screen)
        discipline_select_running200.update(screen)
        discipline_select_jumping.update(screen)
        discipline_select_disc3.update(screen)
        discipline_select_disc4.update(screen)
        back_button.update(screen)

        if discipline_select_running200.check_click(current_state, "countries"):
            util.save_discipline("running")
            util.read_discipline()

        elif discipline_select_jumping.check_click(current_state, "countries"):
            util.save_discipline("jumping")
            util.read_discipline()

        discipline_select_disc3.check_click(current_state, False)
        discipline_select_disc4.check_click(current_state, False)
        back_button.check_click(current_state, "main_menu")
        pygame.display.flip()


running = True


player1_flag = country.Flag(1)
player2_flag = country.Flag(2)

initialization_checker = util.Initialized()
leaderboard_obj = None

while running:
    if current_state.state == "main_menu":
        main_menu()
    if current_state.state == "single_discipline_menu":
        single_discipline_menu()
    if current_state.state == "countries":
        country.countries_select(screen, current_state, player1_flag, player2_flag)

    if current_state.state == "running":
        if initialization_checker.running_initialized is False:
            game = game_running.Game()
            initialization_checker.running_initialized = True
            initialization_checker.leaderboard_initialized = False
        else:
            game.run_game(screen, current_state)
    if current_state.state == "leaderboard":
        if initialization_checker.leaderboard_initialized is False:
            leaderboard_obj = None
            leaderboard_obj = leaderboard.Leaderboard(current_state)
            initialization_checker.leaderboard_initialized = True
            initialization_checker.running_initialized = False
            initialization_checker.jumping_initialized = False
        else:
            leaderboard_obj.run_leaderboard(screen, current_state)
    if current_state.state == "jumping":
        if initialization_checker.jumping_initialized is False:
            game = game_jumping.Game()
            initialization_checker.jumping_initialized = True
            initialization_checker.leaderboard_initialized = False
        else:
            game.run_game(screen)


    clock.tick(FPS)


pygame.quit()
