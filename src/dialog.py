import pygame


class DialogBox:
    X_POSITION = 0
    Y_POSITION = 600

    def __init__(self):
        self.box = pygame.image.load('dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 80))
        self.texts1 = []
        self.texts2 = []
        self.text_index = 0
        self.text_index2 = 0
        self.letter_index = 0
        self.letter_index2 = 0
        self.font = pygame.font.Font('dialogs/dialog_font.ttf', 18)
        self.reading = False

    def execute(self, dialog1=[], dialog2=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.text_index2 = 0
            self.texts1 = dialog1
            self.texts2 = dialog2

    def render(self, screen):
        if self.reading:
            self.letter_index += 1
            self.letter_index2 += 1

            if self.letter_index >= len(self.texts1[self.text_index]):
                self.letter_index = self.letter_index

            if self.letter_index2 >= len(self.texts2[self.text_index2]):
                self.letter_index2 = self.letter_index2

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text1 = self.font.render(self.texts1[self.text_index][0:self.letter_index], False, (0, 0, 0))
            text2 = self.font.render(self.texts2[self.text_index2][0:self.letter_index2], False, (0, 0, 0))
            screen.blit(text1, (self.X_POSITION + 60, self.Y_POSITION + 20))
            screen.blit(text2, (self.X_POSITION + 60, self.Y_POSITION + 40))

    def next_text(self):
        self.text_index += 1
        self.text_index2 += 1
        self.letter_index = 0
        self.letter_index2 = 0

        if self.text_index >= len(self.texts1):
            # close dialog
            self.reading = False
