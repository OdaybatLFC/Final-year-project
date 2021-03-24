"""
Class that represents the menu of the game
"""
import glob
import pygame
from Box import Box


class Menu:

    def __init__(self, window, width, height):
        self.width = width
        self.height = height
        self.window = window
        self.choices = {}
        self.buttons = self.loadButtons()
        self.info_book = self.loadBook()
        self.arg = 0
        self.page = 1

    def draw(self, arg):
        if arg != 3:
            self.window.screen.fill((25, 35, 45))
        if 0 <= arg < 1:
            self.drawButtons(['Play', 'Quit', 'Options'])

        elif arg in [2.2, 3.1, 3.2]:
            if arg == 2.2:
                n = "1"
            elif arg == 3.2:
                n = "2"
            else:
                n = ""
            self.drawText(80, "Choose AI " + n + ":", 3)
            self.drawButtons(["Random", "MiniMax1", "MiniMax2", "MCTS", "Back"])

        elif arg == 2.1:
            self.drawText(80, "Choose player:", 3)
            self.drawButtons(["playerX", "playerO", "Back"])

        elif arg == 3:
            self.drawButtons(["Play again", "Exit"])

        elif arg == 4:
            self.drawText(70, "Game paused", 3)
            self.drawButtons(["Resume", "New Game"])

        elif 1 < arg < 2:
            self.drawText(70, "Choose game mode:", 3)
            self.drawButtons(["Multiplayer", "vs AI", "AI vs AI", "Back"])

        elif arg == 1:
            self.drawButtons(["Game Info", "Fullscreen:", "Back"])

        elif arg == 2:
            self.drawButtons(["Back"])
            if self.page == 1:
                self.drawButtons([">"])
            elif self.page > 13:
                self.drawButtons(["<"])
            else:
                self.drawButtons(["<", ">"])
            self.drawGameInfo(self.page)

    def drawButtons(self, names):
        for name in names:
            button = self.buttons[name]
            button.color = (127, 127, 127)
            button.thickness = 0
            button.paint()
            size = int(button.width / len(name))
            font = pygame.font.SysFont("monospace", size)
            if name == "Fullscreen:":
                if self.window.full_screen:
                    name = name + " ON"
                else:
                    name = name + " OFF"
            text = font.render(name, 1, (255, 255, 0))
            self.window.screen.blit(text, (button.x + button.width / 2 - text.get_rect().width / 2,
                                           button.y + button.height / 2 - text.get_rect().height / 2))
        pygame.display.update()

    def drawText(self, size, text, x):
        font = pygame.font.SysFont("monospace", size)
        text0 = font.render(text, 1, (255, 255, 0))
        self.window.screen.blit(text0, (self.width / 2 - text0.get_rect().width / 2, self.height / x))

    def clearButtons(self):
        for button in self.buttons.values():
            if button.visible:
                button.clear((25, 35, 45))

    def update(self):
        (x, y) = pygame.mouse.get_pos()
        for key in self.buttons:
            button = self.buttons[key]
            if button.onBox(x, y) and button.visible:
                self.animate(key)
                self.clearButtons()
                if key == "Options":
                    self.arg = 1
                    self.draw(1)
                elif key == "Game Info":
                    self.arg = 2
                    self.draw(2)
                elif key in ["<", ">"]:
                    if key == "<":
                        self.page -= 1
                    else:
                        self.page += 1
                    self.draw(2)
                elif key == "New Game":
                    self.arg = 0
                    self.draw(0)
                elif key == "Resume":
                    self.window.screen.fill((25, 35, 45))
                    return 2
                elif key == "Fullscreen:":
                    self.window.updateScreen()
                    # self.drawButtons(['Fullscreen:'])
                elif key in ["Random", "MiniMax1", "MiniMax2", "MCTS"]:
                    if self.arg == 3.1:
                        n = ""
                    elif self.arg == 2.2:
                        n = "1"
                    else:
                        n = "2"
                    if key == "Random":
                        self.choices["AI" + n] = "Random"
                    elif key == "MiniMax1":
                        self.choices["AI" + n] = "M1"
                    if key == "MiniMax2":
                        self.choices["AI" + n] = "M2"
                    elif key == "MCTS":
                        self.choices["AI" + n] = "MCTS"
                    if n == "1":
                        self.arg = 3.2
                        self.draw(3.2)
                    else:
                        self.window.screen.fill((25, 35, 45))
                        return 1
                elif key == "Back":
                    self.arg -= 1
                    self.draw(self.arg)
                elif key == "playerX":
                    self.arg = 3.1
                    self.draw(3.1)
                    self.choices["Player"] = "X"
                elif key == "playerO":
                    self.arg = 3.1
                    self.draw(3.1)
                    self.choices["Player"] = "O"
                elif key == "Multiplayer":
                    self.window.screen.fill((25, 35, 45))
                    self.choices["mode"] = "Multiplayer"
                    return 1
                elif key == "vs AI":
                    self.choices["mode"] = "vs AI"
                    self.arg = 2.1
                    self.draw(2.1)
                elif key == "AI vs AI":
                    self.choices["mode"] = "AI vs AI"
                    self.arg = 2.2
                    self.draw(2.2)
                elif key == "Play":
                    self.arg = 1
                    self.draw(1.1)
                elif key == "Play again":
                    self.draw(0)
                elif key in ["Exit", "Quit"]:
                    return 0
                break

    def animate(self, key):
        pygame.time.set_timer(pygame.USEREVENT, 50)
        iteration = 1
        running = True
        button = self.buttons[key]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if iteration == 1:
                        button.clear((25, 35, 45))
                        button.width -= 5
                        button.height -= 5
                        button.x += 10
                        button.y += 10
                        self.drawButtons([key])
                    elif iteration == 2:
                        button.clear((25, 35, 45))
                        button.width += 5
                        button.height += 5
                        button.x -= 10
                        button.y -= 10
                        self.drawButtons([key])
                    else:
                        running = False
                    iteration += 1

    def winMessage(self, stats):
        self.window.screen.fill((25, 35, 45))
        text = "Player " + str(stats[3][0].id) + " wins!"
        self.drawText(40, text, 7.2)
        self.drawText(40, "Score: " + str(stats[3][0].score) + " - " + str(stats[3][1].score), 2.1)
        self.drawText(40, "Game duration: " + str(stats[2]) + " sec", 3.8)
        self.drawText(40, "Avg time per move(X): " + str(round(sum(stats[1]["X"])/len(stats[1]["X"]), 2)) + " sec", 3)
        self.drawText(40, "Avg time per move(O): " + str(round(sum(stats[1]["O"])/len(stats[1]["O"]), 2)) + " sec", 2.5)
        text = "Moves played: " + str(stats[0]+1)
        self.drawText(40, text, 5)

    def resize(self, size):
        self.width, self.height = size
        self.buttons = self.loadButtons()
        self.info_book = self.loadBook()
        self.draw(self.arg)

    def loadButtons(self):
        return {"Play": Box(self.window, 3 * self.width / 8,
                            3 * self.height / 8, self.width / 4, self.height / 4),
                "Options": Box(self.window, 7 * self.width / 16,
                               1 * self.height / 8, self.width / 8, self.height / 8),
                "Quit": Box(self.window, 7 * self.width / 16,
                            6 * self.height / 8, self.width / 8, self.height / 8),
                "Back": Box(self.window, 7 * self.width / 16,
                            1 * self.height / 8, self.width / 8, self.height / 8),
                "Random": Box(self.window, 1 * self.width / 29,
                              5 * self.height / 8, self.width / 5, self.height / 5),
                "MiniMax1": Box(self.window, 8 * self.width / 29,
                                5 * self.height / 8, self.width / 5, self.height / 5),
                "MiniMax2": Box(self.window, 15 * self.width / 29,
                                5 * self.height / 8, self.width / 5, self.height / 5),
                "MCTS": Box(self.window, 22 * self.width / 29,
                            5 * self.height / 8, self.width / 5, self.height / 5),
                "playerX": Box(self.window, 1 * self.width / 8,
                               5 * self.height / 8, self.width / 4, self.height / 4),
                "playerO": Box(self.window, 5 * self.width / 8,
                               5 * self.height / 8, self.width / 4, self.height / 4),
                "Easy": Box(self.window, 1 * self.width / 16,
                            5 * self.height / 8, self.width / 4, self.height / 4),
                "Normal": Box(self.window, 3 * self.width / 8,
                              5 * self.height / 8, self.width / 4, self.height / 4),
                "Hard": Box(self.window, 11 * self.width / 16,
                            5 * self.height / 8, self.width / 4, self.height / 4),
                "Play again": Box(self.window, 1 * self.width / 8,
                                  5 * self.height / 8, self.width / 4, self.height / 4),
                "Exit": Box(self.window, 5 * self.width / 8,
                            5 * self.height / 8, self.width / 4, self.height / 4),
                "Resume": Box(self.window, 1 * self.width / 8,
                                  5 * self.height / 8, self.width / 4, self.height / 4),
                "New Game": Box(self.window, 5 * self.width / 8,
                            5 * self.height / 8, self.width / 4, self.height / 4),
                "Game Info": Box(self.window, 1 * self.width / 8,
                                 5 * self.height / 8, self.width / 4, self.height / 4),
                "Fullscreen:": Box(self.window, 5 * self.width / 8,
                                   5 * self.height / 8, self.width / 4, self.height / 4),
                "Multiplayer": Box(self.window, 1 * self.width / 16,
                                   5 * self.height / 8, self.width / 4, self.height / 4),
                "vs AI": Box(self.window, 3 * self.width / 8,
                             5 * self.height / 8, self.width / 4, self.height / 4),
                "AI vs AI": Box(self.window, 11 * self.width / 16,
                                5 * self.height / 8, self.width / 4, self.height / 4),
                "<": Box(self.window, self.width / 16,
                         5 * self.height / 9, self.width / 16, self.width / 16),
                ">": Box(self.window, 14 * self.width / 16,
                         5 * self.height / 9, self.width / 16, self.width / 16)}

    def loadBook(self):
        images = glob.glob("img/info/*.png")
        size = int(10 * self.width / 16), int(4 * self.height / 8)
        book = {}
        for image in images:
            img = pygame.image.load(image).convert()
            img = pygame.transform.scale(img, size).convert()
            book[image[9:][:-4]] = img
        return book

    def drawGameInfo(self, p):
        self.window.screen.blit(self.info_book[str(p)], (3 * self.width / 16, 3 * self.height / 8))
        pygame.display.update()
