import util
import pygame

paths = {
    "background": "backgroundfull3.png",
    "running100": "./Assets/single_event_menu/running100.png",
    "running100_active": "./Assets/single_event_menu/running100active.png",
    "hurdles": "./Assets/single_event_menu/hurdles.png",
    "hurdles_active": "./Assets/single_event_menu/hurdlesactive.png",
    "back": "./Assets/single_event_menu/backbutton.png",
    "back_active": "./Assets/single_event_menu/backbuttonactive.png"
}


class SingleDisciplineMenu:
    def __init__(self, screen):
        self.screen = screen
        self.discipline_select_bg = util.Image(paths["background"], (800, 450))
        self.running100 = util.Button(paths["running100"], (800, 300))
        self.hurdles110 = util.Button(paths["hurdles"], (800, 475))
        self.discipline_select_disc3 = util.Button(paths["running100"], (800, 650))
        self.back_button = util.Button(paths["back"], (1410, 835))
        self.back_button.resize(150)
        self.back_button.move(1410, 835)

    def update(self, current_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if self.running100.check_click_and_change_state(current_state, "countries", event):
                util.save_discipline("running")
                util.read_discipline()

            elif self.hurdles110.check_click_and_change_state(current_state, "countries", event):
                util.save_discipline("jumping")
                util.read_discipline()
            self.discipline_select_disc3.check_click_and_change_state(current_state, "running", event)
            self.back_button.check_click_and_change_state(current_state, "main_menu", event)

        self.discipline_select_bg.update(self.screen)

        if self.running100.is_hovering():
            self.running100.set_button_image(paths["running100_active"])
        else:
            self.running100.set_button_image(paths["running100"])
        self.running100.update(self.screen)

        if self.hurdles110.is_hovering():
            self.hurdles110.set_button_image(paths["hurdles_active"])
        else:
            self.hurdles110.set_button_image(paths["hurdles"])
        self.hurdles110.update(self.screen)

        if self.discipline_select_disc3.is_hovering():
            self.discipline_select_disc3.set_button_image(paths["running100_active"])
        else:
            self.discipline_select_disc3.set_button_image(paths["running100"])
        self.discipline_select_disc3.update(self.screen)

        self.back_button.update(self.screen)

        if self.back_button.is_hovering():
            self.back_button.set_button_image(paths["back_active"])
            self.back_button.resize(150)
            self.back_button.move(1410, 835)
        else:
            self.back_button.set_button_image(paths["back"])
            self.back_button.resize(150)
            self.back_button.move(1410, 835)

        pygame.display.flip()
