import pygame
import util
import country
import game_running
import leaderboard
import game_jumping
import ctypes
import single_event_menu
import main_menu

pygame.init()
pygame.font.init()
ctypes.windll.user32.SetProcessDPIAware()

clock = pygame.time.Clock()
FPS = 60
WIDTH = 1600
HEIGHT = 900
MAIN_FONT = "./font/PublicPixel-0W6DP.ttf"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("./Random/logo2whiteoutline.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Mini Olympics")

current_state = util.State()

running = True


main_menu_obj = main_menu.MainMenu(screen)
single_discipline_menu_obj = single_event_menu.SingleDisciplineMenu(screen)

country_selection_obj = country.CountriesSelection()


game = None
leaderboard_obj = None

while running:
    if current_state.state == "main_menu":
        main_menu_obj.update(current_state)
    if current_state.state == "single_discipline_menu":
        single_discipline_menu_obj.update(current_state)
    if current_state.state == "countries":
        country_selection_obj.update(screen, current_state)

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
    if current_state.state != "running" and current_state.state != "jumping":
        clock.tick(30)
    else:
        clock.tick(FPS)

pygame.quit()
