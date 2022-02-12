import util
import pygame

MAIN_FONT = "./font/PublicPixel-0W6DP.ttf"
# Paths
paths = {
    "background": "backgroundfull3.png",
    "single_event": "./Assets/MainMenu/singleevent.png",
    "single_event_active": "./Assets/MainMenu/singleeventactive.png",
    "the_olympics": "./Assets/MainMenu/theolympics.png",
    "the_olympics_active": "./Assets/MainMenu/theolympicsactive.png",
    "settings": "./Assets/MainMenu/settings.png",
    "settings_active": "./Assets/MainMenu/settingsactive.png"

}


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.main_menu_bg = util.Image(paths["background"], 800, 450)

        self.single_discipline_button = util.Button(paths["single_event"], 590, 350, None)
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

    def update(self, current_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.single_discipline_button.check_click(current_state, "single_discipline_menu", event)
            self.the_olympics_button.check_click(current_state, "main_menu", event)
            self.settings_button.check_click(current_state, "single_discipline_menu", event)
            if self.quit_button.check_click(current_state, None, event):
                pygame.quit()

        self.main_menu_bg.update(self.screen)

        if self.single_discipline_button.is_hovering():
            self.single_discipline_button.set_button_image(paths["single_event_active"])
            self.single_event_tooltip.render(self.screen)
        else:
            self.single_discipline_button.set_button_image(paths["single_event"])

        self.single_discipline_button.update(self.screen)

        if self.the_olympics_button.is_hovering():
            self.the_olympics_button.set_button_image("./Assets/MainMenu/theolympicsactive.png")
            self.olympics_tooltip.render(self.screen)
        else:
            self.the_olympics_button.set_button_image("./Assets/MainMenu/theolympics.png")

        self.the_olympics_button.update(self.screen)

        if self.settings_button.is_hovering():
            self.settings_button.set_button_image("./Assets/MainMenu/settingsactive.png")
            self.settings_button_tooltip.render(self.screen)
        else:
            self.settings_button.set_button_image("./Assets/MainMenu/settings.png")

        self.settings_button.update(self.screen)

        if self.quit_button.is_hovering():
            self.quit_button.set_button_image("./Assets/MainMenu/quitactive.png")
            self.quit_button_tooltip.render(self.screen)
        else:
            self.quit_button.set_button_image("./Assets/MainMenu/quit.png")


        self.quit_button.update(self.screen)

        pygame.display.flip()
