import util
import pygame


class SingleDisciplineMenu:
    def __init__(self, screen):
        self.screen = screen
        self.discipline_select_bg = util.Image("backgroundfull3.png", 800, 450)
        self.running100 = util.Button("./Assets/SingleEventMenu/running100.png", 800, 300, None)
        self.hurdles110 = util.Button("./Assets/SingleEventMenu/hurdles.png", 800, 475, None)
        self.discipline_select_disc3 = util.Button("./Assets/SingleEventMenu/running100.png", 800, 650, None)
        self.back_button = util.Button("./Assets/SingleEventMenu/backbutton.png", 1410, 835, None)
        self.back_button.resize(150)
        self.back_button.move(1410, 835)

    def update(self, current_state):
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

        self.discipline_select_bg.update(self.screen)

        if self.running100.is_hovering():
            self.running100.set_button_image("./Assets/SingleEventMenu/running100active.png")
        else:
            self.running100.set_button_image("./Assets/SingleEventMenu/running100.png")
        self.running100.update(self.screen)

        if self.hurdles110.is_hovering():
            self.hurdles110.set_button_image("./Assets/SingleEventMenu/hurdlesactive.png")
        else:
            self.hurdles110.set_button_image("./Assets/SingleEventMenu/hurdles.png")
        self.hurdles110.update(self.screen)

        if self.discipline_select_disc3.is_hovering():
            self.discipline_select_disc3.set_button_image("./Assets/SingleEventMenu/running100active.png")
        else:
            self.discipline_select_disc3.set_button_image("./Assets/SingleEventMenu/running100.png")
        self.discipline_select_disc3.update(self.screen)

        self.back_button.update(self.screen)

        if self.back_button.is_hovering():
            self.back_button.set_button_image("./Assets/SingleEventMenu/backbuttonactive.png")
            self.back_button.resize(150)
            self.back_button.move(1410, 835)
        else:
            self.back_button.set_button_image("./Assets/SingleEventMenu/backbutton.png")
            self.back_button.resize(150)
            self.back_button.move(1410, 835)

        pygame.display.flip()