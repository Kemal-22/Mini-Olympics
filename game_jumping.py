import pygame
import util

MAIN_FONT = "./Assets/fonts/PublicPixel-0W6DP.ttf"
WHITE = (255, 255, 255)


class ProceduralText:
    def __init__(self, font, font_size, text, color):
        self.color = color
        self.font = pygame.font.Font(font, font_size)
        self.text_surface = self.font.render(text, False, self.color)
        self.position_temp = (0, 0)
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()
        self.position = (self.position_temp[0] - (self.text_width / 2), self.position_temp[1] - (self.text_height / 2))
        self.cap_center = util.Image("text_center.png", 0, 0)
        self.cap_left = util.Image("text_cap_left.png", 0, 0)
        self.cap_right = util.Image("text_cap_right.png", 0, 0)
        self.update_caps()

    def move_text(self, position_x, position_y):
        temp = (position_x, position_y)
        self.position = (temp[0] - (self.text_width / 2), temp[1] - (self.text_height / 2))
        self.update_caps()

    def get_center(self):
        position_top_left = (self.position[0] + (self.text_width / 2), self.position[1] + (self.text_height / 2))
        return position_top_left

    def change_text(self, text):
        top_left = self.get_center()
        self.text_surface = self.font.render(text, False, self.color)
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()
        self.move_text(top_left[0], top_left[1])
        self.update_caps()

    def update_caps(self):
        # Update center cap
        position = self.get_center()
        center_cap_percentage = 100 / (self.cap_center.get_image_width() / self.text_surface.get_width())
        self.cap_center.resize(center_cap_percentage)
        self.cap_center.move(position[0], position[1])

        # Update left cap
        center = self.get_center()
        self.cap_left.resize(center_cap_percentage)
        position_x = (center[0] - (self.cap_center.get_image_width() / 2)) - (self.cap_left.get_image_width() / 2)
        position_y = center[1]
        self.cap_left.move(position_x, position_y)

        # Update right cap
        center = self.get_center()
        self.cap_right.resize(center_cap_percentage)
        position_x = (center[0] + (self.cap_center.get_image_width() / 2)) + (self.cap_right.get_image_width() / 2)
        position_y = center[1]
        self.cap_right.move(position_x, position_y)

    def display_text(self, screen):
        self.cap_center.update(screen)
        self.cap_left.update(screen)
        self.cap_right.update(screen)
        screen.blit(self.text_surface, self.position)


class Game:
    def __init__(self):
        self.text = ProceduralText(MAIN_FONT, 75, "Test123", WHITE)
        self.text.move_text(800, 400)
        self.text.move_text(1200, 400)
        self.text.change_text("Kemica je legenda!")
        self.text.move_text(800, 400)

    def run_game(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.text.display_text(screen)
        pygame.display.flip()
