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
MAIN_FONT = "./font/PublicPixel-0W6DP.ttf"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("logo2whiteoutline.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Mini Olympics")

def test_func():
    #print("Working")
    pass


def test_func2():
    print("Working too")


class MainMenu:
    def __init__(self):
        self.main_menu_bg = util.Image("backgroundfull3.png", 800, 450)

        self.single_discipline_button = util.Button("./Assets/MainMenu/singleevent.png", 590, 350, None)
        self.single_event_tooltip = util.Text("Choose and play a single event from the olympics.", (50, 800),
                                              MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.single_event_tooltip.set_position((30 + self.single_event_tooltip.width / 2, 865))

        self.the_olympics_button = util.Button("./Assets/MainMenu/theolympics.png", 1010, 350, None)
        self.olympics_tooltip = util.Text("Compete in all olympic events.", (50, 800),
                                              MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.olympics_tooltip.set_position((30 + self.olympics_tooltip.width / 2, 865))

        self.settings_button = util.Button("./Assets/MainMenu/settings.png", 590, 610, None)
        self.settings_button_tooltip = util.Text("Adjust the game's settings.", (50, 800),
                                          MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.settings_button_tooltip.set_position((30 + self.settings_button_tooltip.width / 2, 865))

        self.quit_button = util.Button("./Assets/MainMenu/quit.png", 1010, 610, None)
        self.quit_button_tooltip = util.Text("Quit the game.", (50, 800),
                                                 MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.quit_button_tooltip.set_position((30 + self.quit_button_tooltip.width / 2, 865))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.single_discipline_button.check_click(current_state, "single_discipline_menu", event)
            self.the_olympics_button.check_click(current_state, "main_menu", event)
            self.settings_button.check_click(current_state, "single_discipline_menu", event)
            if self.quit_button.check_click(current_state, None, event):
                pygame.quit()

        self.main_menu_bg.update(screen)

        if self.single_discipline_button.is_hovering():
            self.single_discipline_button.set_button_image("./Assets/MainMenu/singleeventactive.png")
            self.single_event_tooltip.render(screen)
        else:
            self.single_discipline_button.set_button_image("./Assets/MainMenu/singleevent.png")

        self.single_discipline_button.update(screen)

        if self.the_olympics_button.is_hovering():
            self.the_olympics_button.set_button_image("./Assets/MainMenu/theolympicsactive.png")
            self.olympics_tooltip.render(screen)
        else:
            self.the_olympics_button.set_button_image("./Assets/MainMenu/theolympics.png")

        self.the_olympics_button.update(screen)

        if self.settings_button.is_hovering():
            self.settings_button.set_button_image("./Assets/MainMenu/settingsactive.png")
            self.settings_button_tooltip.render(screen)
        else:
            self.settings_button.set_button_image("./Assets/MainMenu/settings.png")

        self.settings_button.update(screen)

        if self.quit_button.is_hovering():
            self.quit_button.set_button_image("./Assets/MainMenu/quitactive.png")
            self.quit_button_tooltip.render(screen)
        else:
            self.quit_button.set_button_image("./Assets/MainMenu/quit.png")


        self.quit_button.update(screen)

        pygame.display.flip()


class SingleDisciplineMenu:
    def __init__(self):
        screen.fill((255, 255, 255))
        self.discipline_select_bg = util.Image("backgroundfull3.png", 800, 450)
        self.running100 = util.Button("./Assets/SingleEventMenu/running100.png", 800, 300, None)
        self.hurdles110 = util.Button("./Assets/SingleEventMenu/hurdles.png", 800, 475, None)
        self.discipline_select_disc3 = util.Button("./Assets/SingleEventMenu/running100.png", 800, 650, None)
        self.back_button = util.Button("./Assets/SingleEventMenu/backbutton.png", 1410, 835, None)
        self.back_button.resize(150)
        self.back_button.move(1410, 835)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if self.running100.check_click(current_state, "countries", event):
                util.save_discipline("running")
                util.read_discipline()

            elif self.hurdles110.check_click(current_state, "countries", event):
                util.save_discipline("jumping")
                util.read_discipline()
            self.discipline_select_disc3.check_click(current_state, False, event)
            self.back_button.check_click(current_state, "main_menu", event)

        self.discipline_select_bg.update(screen)

        if self.running100.is_hovering():
            self.running100.set_button_image("./Assets/SingleEventMenu/running100active.png")
        else:
            self.running100.set_button_image("./Assets/SingleEventMenu/running100.png")
        self.running100.update(screen)

        if self.hurdles110.is_hovering():
            self.hurdles110.set_button_image("./Assets/SingleEventMenu/hurdlesactive.png")
        else:
            self.hurdles110.set_button_image("./Assets/SingleEventMenu/hurdles.png")
        self.hurdles110.update(screen)

        if self.discipline_select_disc3.is_hovering():
            self.discipline_select_disc3.set_button_image("./Assets/SingleEventMenu/running100active.png")
        else:
            self.discipline_select_disc3.set_button_image("./Assets/SingleEventMenu/running100.png")
        self.discipline_select_disc3.update(screen)

        self.back_button.update(screen)

        if self.back_button.is_hovering():
            self.back_button.set_button_image("./Assets/SingleEventMenu/backbuttonactive.png")
            self.back_button.resize(150)
            self.back_button.move(1410, 835)
        else:
            self.back_button.set_button_image("./Assets/SingleEventMenu/backbutton.png")
            self.back_button.resize(150)
            self.back_button.move(1410, 835)

        pygame.display.flip()


current_state = util.State()

running = True

player1_flag = country.Flag(1)
player2_flag = country.Flag(2)

initialization_checker = util.Initialized()
single_discipline_menu_obj = SingleDisciplineMenu()
country_selection_obj = country.CountriesSelection(player1_flag, player2_flag)
main_menu_obj = MainMenu()

game = None
leaderboard_obj = None

while running:
    if current_state.state == "main_menu":
        main_menu_obj.update()
    if current_state.state == "single_discipline_menu":
        single_discipline_menu_obj.update()
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
