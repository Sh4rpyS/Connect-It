import pygame, game, user, levels, editor, grid
from pygame.locals import *

pygame.init()

# Text class can be used to create text objects that can be drawn on the screen
class Text:
    texts = {}
    fonts = {}

    def __init__(self, name: str, scene: str, x: float, y: float, text: str, size: int, alignment: str = "none") -> None:
        self.name = name
        self.scene = scene
        self.original_x = x
        self.original_y = y
        self.text = str(text)
        self.size = size
        self.alignment = alignment
        self.active = True
        self.visible = True

        # Add itself to the text object list
        Text.texts[self.name] = self # To delete the text object, just remove it from the list

        # Create a new font object, if one is not found
        if not self.size in Text.fonts:
            Text.fonts[self.size] = pygame.font.Font("fonts/arial.ttf", self.size)

        # White color for the text is hardcoded, atleast for now
        self.object = Text.fonts[self.size].render(self.text, True, (255, 255, 255))

        self.update_text(self.text)
        
    def update_text(self, text: str) -> None: # Updates the text of the object
        self.text = str(text)
        # Make the required alignments
        if self.alignment == "center":
            object_size = Text.fonts[self.size].size(self.text)
            self.x = self.original_x - object_size[0] / 2
            self.y = self.original_y - object_size[1] / 2
        elif self.alignment == "right":
            object_size = Text.fonts[self.size].size(self.text)
            self.x = self.original_x - object_size[0]
            self.y = self.original_y
        else:
            self.x = self.original_x
            self.y = self.original_y

        self.object = Text.fonts[self.size].render(self.text, True, (255, 255, 255))

    def set_active(self, active: bool) -> None:
        self.active = active
    
    def draw(self) -> None: # Draws the objects correct for the scene
        if self.scene == game.scene and self.active and self.visible:
            game.screen.blit(self.object, (self.x, self.y))

class InputBox:
    inputboxes = {}
    targeted = ""

    def __init__(self, name: str, scene: str, x: float, y: float, width: int, height: int, placeholder: str, size: int, max_characters: int) -> None:
        self.name = name
        self.scene = scene
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True
        self.visible = True

        # Text elements
        self.placeholder = placeholder
        self.text = placeholder
        self.text_size = size
        self.max_characters = max_characters

        InputBox.inputboxes[self.name] = self
        self.text_x = self.x + self.width/2
        self.text_y = self.y + self.height/2
        Text(f"{self.name}_inputbox", "editor", self.text_x, self.text_y, self.text, self.text_size, alignment="center")

        # Create the inputbox objects
        horizontal = pygame.Surface((self.width, 4))
        vertical = pygame.Surface((4, self.height))

        # Create main the inputbox object
        self.input_box = pygame.Surface((self.width, self.height))
        horizontal.fill((255, 255, 255))
        vertical.fill((255, 255, 255))
        self.input_box.blit(horizontal, (0, 0))
        self.input_box.blit(horizontal, (0, self.height-4))
        self.input_box.blit(vertical, (0, 0))
        self.input_box.blit(vertical, (self.width-4, 0))

        # Create the highlight for the inputbox
        self.input_box_highlighted = pygame.Surface((self.width, self.height))
        horizontal.fill((150, 150, 150))
        vertical.fill((150, 150, 150))
        self.input_box_highlighted.blit(horizontal, (0, 0))
        self.input_box_highlighted.blit(horizontal, (0, self.height-4))
        self.input_box_highlighted.blit(vertical, (0, 0))
        self.input_box_highlighted.blit(vertical, (self.width-4, 0))

        # Create the targeted for the inputbox
        self.input_box_targeted = pygame.Surface((self.width, self.height))
        horizontal.fill((80, 80, 80))
        vertical.fill((80, 80, 80))
        self.input_box_targeted.blit(horizontal, (0, 0))
        self.input_box_targeted.blit(horizontal, (0, self.height-4))
        self.input_box_targeted.blit(vertical, (0, 0))
        self.input_box_targeted.blit(vertical, (self.width-4, 0))

        self.object = game.screen.blit(self.input_box, (self.x, self.y))

    def set_active(self, active: bool) -> None:
        self.active = active
        Text.texts[f"{self.name}_inputbox"].active = active

    def draw(self) -> None:
        if self.scene == game.scene and self.active and self.visible:
            if self.name == InputBox.targeted:
                self.object = game.screen.blit(self.input_box_targeted, (self.x, self.y))
            elif self.object.collidepoint(game.mouse_pos):
                self.object = game.screen.blit(self.input_box_highlighted, (self.x, self.y))
            else:
                self.object = game.screen.blit(self.input_box, (self.x, self.y))

class Button:
    buttons = {}

    def __init__(self, name: str, scene: str, x: float, y: float, width: int, height: int, text: str, text_size: int, text_alignment: str = "none", button_alignemnt: str = "none") -> None:
        self.name = name
        self.scene = scene
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = str(text)
        self.text_size = text_size
        self.text_alignment = text_alignment
        self.button_alignemnt = button_alignemnt
        self.active = True
        self.visible = True

        self.txt_x = self.x
        self.txt_y = self.y

        if self.button_alignemnt == "center":
            self.x -= self.width / 2
            self.y -= self.height / 2
        elif self.button_alignemnt == "right":
            self.x -= self.width

        if self.text_alignment == "none" or self.text_alignment == "left":
            self.txt_x += self.width / 20
            self.txt_y += self.height / 4

        # Add itself to the text object list
        Button.buttons[self.name] = self

        horizontal = pygame.Surface((self.width, 4))
        vertical = pygame.Surface((4, self.height))

        # Create the button object
        self.button_object = pygame.Surface((self.width, self.height))
        horizontal.fill((255, 255, 255))
        vertical.fill((255, 255, 255))
        self.button_object.blit(horizontal, (0, 0))
        self.button_object.blit(horizontal, (0, self.height-4))
        self.button_object.blit(vertical, (0, 0))
        self.button_object.blit(vertical, (self.width-4, 0))

        # Create the highlight for the button
        self.button_object_highlight = pygame.Surface((self.width, self.height))
        horizontal.fill((150, 150, 150))
        vertical.fill((150, 150, 150))
        self.button_object_highlight.blit(horizontal, (0, 0))
        self.button_object_highlight.blit(horizontal, (0, self.height-4))
        self.button_object_highlight.blit(vertical, (0, 0))
        self.button_object_highlight.blit(vertical, (self.width-4, 0))

        self.object = game.screen.blit(self.button_object, (self.x, self.y))

        # Create the object that is created for the button
        self.button_text = Text(f"{self.name}_button", self.scene, self.txt_x, self.txt_y, self.text, self.text_size, self.text_alignment)

    def set_active(self, active: bool) -> None:
        self.active = active
        Text.texts[f"{self.name}_button"].active = active

    def draw(self) -> None: # Draws the objects correct for the scene
        if self.scene == game.scene and self.active and self.visible:
            if self.object.collidepoint(game.mouse_pos): game.screen.blit(self.button_object_highlight, (self.x, self.y))
            else: game.screen.blit(self.button_object, (self.x, self.y))

def Draw() -> None:
    for button in Button.buttons.values(): # Draws the button objects
        button.draw()
    for inputbox in InputBox.inputboxes.values(): # Draws the input field objects
        inputbox.draw()
    for text in Text.texts.values(): # Draws the text objects
        text.draw()

def Button_Functionality() -> None:
    # Not really a button, but InputBox targeting is also checked here
    for input_box in InputBox.inputboxes.values():
        if input_box.object.collidepoint(game.mouse_pos) and input_box.scene == game.scene and input_box.active:
            if input_box.name != InputBox.targeted: InputBox.targeted = input_box.name
            else: InputBox.targeted = ""
            break

    for button in Button.buttons.values():
        if button.object.collidepoint(game.mouse_pos) and button.scene == game.scene and button.active:
            InputBox.targeted = ""
            match(button.name):
                case "play": 
                    game.scene = "levels"
                    break
                case "editor": 
                    game.scene = "editor"
                    break
                case "game_to_menu": 
                    user.User.loaded_level = 0
                    game.scene = "menu"
                    break
                case "editor_to_menu": 
                    game.scene = "menu"
                    editor.highlight_x = 999
                    editor.selected_color = (0, 0, 0)
                    break
                case "game_to_levels": 
                    user.User.loaded_level = 0
                    game.scene = "levels"
                    break
                case "exit": 
                    game.End_Game()
                    break
                case "page_up": 
                    levels.Page_Up()
                    break
                case "page_down": 
                    levels.Page_Down()
                    break
                case "levels_back":
                    user.User.loaded_level = 0
                    game.scene = "menu"
                    break
                case "levels_play":
                    if levels.selected_index != 10 and levels.level_name != "":
                        user.Load_Level(levels.level_name)
                        game.scene = "game"
                    break
                case "editor_settings":
                    editor.Toggle_Settings()
                    break
                case "editor_level_size_up":
                    editor.Increase_Level_Size()
                    break
                case "editor_level_size_down":
                    editor.Decrease_Level_Size()
                    break
                case "editor_level_up":
                    editor.Increase_Level()
                    break
                case "editor_level_down":
                    editor.Decrease_Level()
                    break
                case "editor_save_pack":
                    editor.Save_Pack(Text.texts["editor_pack_name_inputbox"].text)
                    break
                case "editor_load_pack":
                    editor.Load_Pack(Text.texts["editor_pack_name_inputbox"].text)
                    break
                case "continue":
                    user.User.loaded_level += 1
                    if user.User.loaded_level+1 == user.User.max_levels:
                        game.scene = "levels"
                        user.User.loaded_level = 0
                    else:
                        user.Load_Level(user.User.loaded_pack)
                        grid.Count_Level_Completion()

    
    if game.scene == "levels":
        for button in levels.pack_buttons:
            if button.object.collidepoint(game.mouse_pos) and button.scene == game.scene and button.active:
                if levels.selected_index != levels.pack_buttons.index(button): levels.selected_index = levels.pack_buttons.index(button)
                else: levels.selected_index = 10
    elif game.scene == "editor":
        for color_button in editor.ColorButton.color_buttons:
            if color_button.object.collidepoint(game.mouse_pos):
                if editor.selected_color == color_button.color:
                    editor.highlight_x = 999
                    editor.selected_color = (0, 0, 0)
                else:
                    editor.highlight_x = color_button.x - 4
                    editor.selected_color = color_button.color

def Input_Box_Functionality(key, mod) -> None:
    letter = ""

    if key == pygame.K_a: letter = "a"
    elif key == pygame.K_b: letter = "b"
    elif key == pygame.K_c: letter = "c"
    elif key == pygame.K_d: letter = "d"
    elif key == pygame.K_e: letter = "e"
    elif key == pygame.K_f: letter = "f"
    elif key == pygame.K_g: letter = "g"
    elif key == pygame.K_h: letter = "h"
    elif key == pygame.K_i: letter = "i"
    elif key == pygame.K_j: letter = "j"
    elif key == pygame.K_k: letter = "k"
    elif key == pygame.K_l: letter = "l"
    elif key == pygame.K_m: letter = "m"
    elif key == pygame.K_n: letter = "n"
    elif key == pygame.K_o: letter = "o"
    elif key == pygame.K_p: letter = "p"
    elif key == pygame.K_q: letter = "q"
    elif key == pygame.K_r: letter = "r"
    elif key == pygame.K_s: letter = "s"
    elif key == pygame.K_t: letter = "t"
    elif key == pygame.K_u: letter = "u"
    elif key == pygame.K_v: letter = "v"
    elif key == pygame.K_w: letter = "w"
    elif key == pygame.K_x: letter = "x"
    elif key == pygame.K_y: letter = "y"
    elif key == pygame.K_z: letter = "z"
    elif key == pygame.K_0: letter = "0"
    elif key == pygame.K_1: letter = "1"
    elif key == pygame.K_2: letter = "2"
    elif key == pygame.K_3: letter = "3"
    elif key == pygame.K_4: letter = "4"
    elif key == pygame.K_5: letter = "5"
    elif key == pygame.K_6: letter = "6"
    elif key == pygame.K_7: letter = "7"
    elif key == pygame.K_8: letter = "8"
    elif key == pygame.K_9: letter = "9"
    elif key == pygame.K_SPACE: letter = " "

    if key == pygame.K_BACKSPACE:
        updated_text = Text.texts[f"{InputBox.targeted}_inputbox"].text[0:-1]
        Text.texts[f"{InputBox.targeted}_inputbox"].update_text(updated_text)
    else:
        if mod & pygame.KMOD_CAPS:
            if mod & pygame.KMOD_SHIFT: letter = letter.lower()
            else: letter = letter.upper()
        elif mod & pygame.KMOD_SHIFT: letter = letter.upper()
        
        if letter != "":
            updated_text = Text.texts[f"{InputBox.targeted}_inputbox"].text + letter
            if len(updated_text) <= InputBox.inputboxes[InputBox.targeted].max_characters:
                Text.texts[f"{InputBox.targeted}_inputbox"].update_text(updated_text)