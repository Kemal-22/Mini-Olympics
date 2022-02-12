import util
import pygame

MAIN_FONT = "./Assets/fonts/PublicPixel-0W6DP.ttf"
# Paths
paths = {
    "background": "backgroundfull3.png",
    "single_event": "./Assets/main_menu/singleevent.png",
    "single_event_active": "./Assets/main_menu/singleeventactive.png",
    "the_olympics": "./Assets/main_menu/theolympics.png",
    "the_olympics_active": "./Assets/main_menu/theolympicsactive.png",
    "settings": "./Assets/main_menu/settings.png",
    "settings_active": "./Assets/main_menu/settingsactive.png",
    "quit": "./Assets/main_menu/quit.png",
    "quit_active": "./Assets/main_menu/quitactive.png"

}


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.main_menu_bg = util.Image(paths["background"], (800, 450))

        self.single_discipline_button = util.Button(paths["single_event"], (590, 350))
        self.single_event_tooltip = util.Text("Choose and play a single event from the olympics.", (50, 800),
                                              MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.single_event_tooltip.set_position((30 + self.single_event_tooltip.width / 2, 865))

        self.the_olympics_button = util.Button(paths["the_olympics"], (1010, 350))
        self.olympics_tooltip = util.Text("Compete in all olympic events.", (50, 800),
                                              MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.olympics_tooltip.set_position((30 + self.olympics_tooltip.width / 2, 865))

        self.settings_button = util.Button(paths["settings"], (590, 610))
        self.settings_button_tooltip = util.Text("Adjust the game's settings.", (50, 800),
                                          MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.settings_button_tooltip.set_position((30 + self.settings_button_tooltip.width / 2, 865))

        self.quit_button = util.Button(paths["quit"], (1010, 610))
        self.quit_button_tooltip = util.Text("Quit the game.", (50, 800),
                                                 MAIN_FONT, color=(255, 255, 255), font_size=24)
        self.quit_button_tooltip.set_position((30 + self.quit_button_tooltip.width / 2, 865))

    def update(self, current_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.single_discipline_button.check_click_and_change_state(current_state, "single_discipline_menu", event)
            self.the_olympics_button.check_click_and_change_state(current_state, "main_menu", event)
            self.settings_button.check_click_and_change_state(current_state, "single_discipline_menu", event)
            if self.quit_button.check_click(event):
                pygame.quit()

        self.main_menu_bg.update(self.screen)

        if self.single_discipline_button.is_hovering():
            self.single_discipline_button.set_button_image(paths["single_event_active"])
            self.single_event_tooltip.render(self.screen)
        else:
            self.single_discipline_button.set_button_image(paths["single_event"])

        self.single_discipline_button.update(self.screen)

        if self.the_olympics_button.is_hovering():
            self.the_olympics_button.set_button_image(paths["the_olympics_active"])
            self.olympics_tooltip.render(self.screen)
        else:
            self.the_olympics_button.set_button_image(paths["the_olympics"])

        self.the_olympics_button.update(self.screen)

        if self.settings_button.is_hovering():
            self.settings_button.set_button_image(paths["settings_active"])
            self.settings_button_tooltip.render(self.screen)
        else:
            self.settings_button.set_button_image(paths["settings"])

        self.settings_button.update(self.screen)

        if self.quit_button.is_hovering():
            self.quit_button.set_button_image(paths["quit_active"])
            self.quit_button_tooltip.render(self.screen)
        else:
            self.quit_button.set_button_image(paths["quit"])

        self.quit_button.update(self.screen)

        pygame.display.flip()
