import pygame, grid, game, dot, interface, os
pygame.init()

class ColorButton:
    color_buttons = []

    def __init__(self, x: float, y: float, color: tuple) -> None:
        self.x = x
        self.y = y
        self.color = color

        ColorButton.color_buttons.append(self)

        self.color_button = pygame.Surface((28, 28))
        self.color_button.fill(self.color)

        self.object = game.screen.blit(self.color_button, (self.x-1, self.y-1))

    def draw(self) -> None:
        self.object = game.screen.blit(self.color_button, (self.x-1, self.y-1))

# Runs once when the game starts
def Init() -> None:
    global selected_color, settings_open, settings_ui, editor_level_size, level_number, pack, highlight_x

    pack = {1: [5]}
    settings_ui = []

    level_number = 1
    editor_level_size = pack[level_number][0]

    interface.Button("editor_to_menu", "editor", 102, 30, 162, 40, "MENU", 28, text_alignment="center", button_alignemnt="center")
    interface.Button("editor_settings", "editor", 102, 85, 162, 40, "SETTINGS", 28, text_alignment="center", button_alignemnt="center")
    interface.Text("editor_color_picker_header", "editor", 386, 35, "Color Picker", 32, alignment="center")

    # Settings UI
    settings_ui.append(interface.Text("editor_settings_text", "editor", 300, 170, "Settings", 52, alignment="center"))
    settings_ui.append(interface.Text("editor_pack_settings_text", "editor", 75, 200, "Pack Settings", 42, alignment="none"))
    settings_ui.append(interface.Text("editor_level_settings_text", "editor", 75, 430, "Level Settings", 42, alignment="none"))

    settings_ui.append(interface.Text("editor_pack_name_header", "editor", 80, 270, "Pack Name: ", 32, alignment="none"))
    #settings_ui.append(interface.Button("editor_pack_name_temp", "editor", 390, 307, 240, 50, "", 24, text_alignment="center", button_alignemnt="center"))
    settings_ui.append(interface.InputBox("editor_pack_name", "editor", 80, 307, 430, 50, "", 24, 20))
    settings_ui.append(interface.Button("editor_save_pack", "editor", 185, 387, 210, 40, "SAVE PACK", 28, text_alignment="center", button_alignemnt="center"))
    settings_ui.append(interface.Button("editor_load_pack", "editor", 405, 387, 210, 40, "LOAD PACK", 28, text_alignment="center", button_alignemnt="center"))

    settings_ui.append(interface.Text("editor_level_text", "editor", 390, 523, f"{level_number}", 32, alignment="center"))
    settings_ui.append(interface.Text("editor_level_text_header", "editor", 80, 506, "Level: ", 32, alignment="none"))
    settings_ui.append(interface.Button("editor_level_up", "editor", 490, 523, 40, 40, ">", 32, text_alignment="center", button_alignemnt="center"))
    settings_ui.append(interface.Button("editor_level_down", "editor", 290, 523, 40, 40, "<", 32, text_alignment="center", button_alignemnt="center"))

    settings_ui.append(interface.Text("editor_level_size_text", "editor", 390, 593, f"{editor_level_size}x{editor_level_size}", 32, alignment="center"))
    settings_ui.append(interface.Text("editor_level_size_text_header", "editor", 80, 576, "Level Size: ", 32, alignment="none"))
    settings_ui.append(interface.Button("editor_level_size_up", "editor", 490, 593, 40, 40, ">", 32, text_alignment="center", button_alignemnt="center"))
    settings_ui.append(interface.Button("editor_level_size_down", "editor", 290, 593, 40, 40, "<", 32, text_alignment="center", button_alignemnt="center"))
    
    # Declare the colors
    colors = [(80, 0, 0), (255, 0, 0), (0, 127, 0), (0, 255, 0), (0, 0, 127), (0, 0, 255),
    (255, 0, 127), (255, 0, 255), (127, 0, 127), (90, 60, 40), (180, 120, 80), (127, 127, 127),
    (255, 255, 255), (255, 127, 0), (255, 216, 0)]

    # Initialize the color buttons
    for i in range(15):
        ColorButton(199 + 25 * i, 61, colors[i])

    selected_color = (0, 0, 0)
    highlight_x = 999
    
    settings_open = True

    Toggle_Settings()

# Used to toggle UI objects on and off
def Toggle_Settings() -> None:
    global settings_open

    if settings_open:
        settings_open = False

        # Disable all the UI objects that are in the settings panel
        for ui_object in settings_ui:
            ui_object.set_active(False)
    else:
        settings_open = True

        # Enable all the UI objects that are in the settings panel
        for ui_object in settings_ui:
            ui_object.set_active(True)

# Changes level up
def Increase_Level() -> None:
    global level_number, editor_level_size, pack
    level_number += 1

    # Create a new level
    if not level_number in pack.keys():
        editor_level_size = 5
        pack[level_number] = [editor_level_size]

    editor_level_size = pack[level_number][0]
    interface.Text.texts["editor_level_text"].update_text(f"{level_number}")
    interface.Text.texts["editor_level_size_text"].update_text(f"{editor_level_size}x{editor_level_size}")

    dot.EditorDot.dots.clear()
    for i in range(1, len(pack[level_number])):
        dot.EditorDot.dots.append(pack[level_number][i])


# Changes level down
def Decrease_Level() -> None:
    global level_number, editor_level_size, pack
    if level_number > 1:
        if len(pack[level_number]) == 1: pack.pop(level_number)
        level_number -= 1
        editor_level_size = pack[level_number][0]
        interface.Text.texts["editor_level_text"].update_text(f"{level_number}")
        interface.Text.texts["editor_level_size_text"].update_text(f"{editor_level_size}x{editor_level_size}")

        dot.EditorDot.dots.clear()
        for i in range(1, len(pack[level_number])):
            dot.EditorDot.dots.append(pack[level_number][i])

# Changes level size up
def Increase_Level_Size() -> None:
    global editor_level_size, pack

    if editor_level_size < 10:
        editor_level_size += 1
        interface.Text.texts["editor_level_size_text"].update_text(f"{editor_level_size}x{editor_level_size}")

        pack[level_number][0] = editor_level_size

        for dot_object in dot.EditorDot.dots:
            dot_object.update_dot(dot_object.original_x, dot_object.original_y, dot_object.color, editor_level_size)

# Changes level size down
def Decrease_Level_Size() -> None:
    global editor_level_size, pack

    if editor_level_size > 2:
        editor_level_size -= 1
        interface.Text.texts["editor_level_size_text"].update_text(f"{editor_level_size}x{editor_level_size}")

        pack[level_number][0] = editor_level_size

        dots_outside = []

        for dot_object in dot.EditorDot.dots:
            dot_object.update_dot(dot_object.original_x, dot_object.original_y, dot_object.color, editor_level_size)

            if dot_object.original_x+1 > editor_level_size or dot_object.original_y+1 > editor_level_size:
                dots_outside.append(dot_object)

        for dot_object in dots_outside:
            dot.EditorDot.dots.remove(dot_object)

def Draw_Color_Picker() -> None:
    # Draw the border for the color picker
    pygame.draw.rect(game.screen, (255, 255, 255), (195, 57, 383, 33), width = 4)

    # Draws all the color buttons
    for color_button in ColorButton.color_buttons:
        color_button.draw()

    # Draw the small grid
    for i in range(14):
        pygame.draw.line(game.screen, (255, 255, 255), (223 + i * 25, 60), (223 + i * 25, 88), width = 2)

    pygame.draw.rect(game.screen, (200, 200, 200), (highlight_x, 57, 33, 33), width = 4)

def Convert_Mouse_To_Editor() -> None:
    x = ((game.mouse_pos[0]-25) / 55) % (550 / editor_level_size) / (10/editor_level_size)
    y = ((game.mouse_pos[1]-125) / 55) % (550 / editor_level_size) / (10/editor_level_size)

    return (int(x), int(y))

def Create_New_Dot() -> None:
    if game.mouse_pos[0] > 25 and game.mouse_pos[0] < 575 and game.mouse_pos[1] > 125 and game.mouse_pos[1] < 675:
        collision = False

        for dot_object in dot.EditorDot.dots:
            if dot_object.collider_obj.collidepoint(game.mouse_pos):
                dot.EditorDot.dots.remove(dot_object)
                pack[level_number].remove(dot_object)
                collision = True
                break
        
        if not collision and selected_color != (0, 0, 0):
            dot_pos = Convert_Mouse_To_Editor()
            new_dot = dot.EditorDot(dot_pos[0], dot_pos[1], selected_color, editor_level_size)
            pack[level_number].append(new_dot)

def Save_Pack(pack_name: str) -> None:
    if pack_name != "":
        with open(f"levels/{pack_name}.cpk", "w") as f:
            for level_data in pack.items():
                # If the level is empty skip it
                if len(level_data[1]) == 1:
                    continue

                level_num = level_data[0]
                level_size = level_data[1][0]
                f.write(f"{level_num};{level_size};\n")
                for i in range(1, len(level_data[1])):
                    dot = level_data[1][i]
                    f.write(f"{dot.color}.{dot.original_x}.{dot.original_y};")
                f.write("\n:\n")

def Load_Pack(pack_name: str) -> None:
    global level_number, editor_level_size, pack

    packs = os.listdir("levels")

    if f"{pack_name}.cpk" in packs:
        pack.clear()
        dot.EditorDot.dots.clear()

        with open(f"levels/{pack_name}.cpk", "r") as f:
            pack_data = f.read().replace("\n", "").split(":")

        for i in range(len(pack_data)-1):
            level = pack_data[i].split(";")
            level_num = int(level[0])
            level_size = int(level[1])

            pack[level_num] = [level_size]

            for i in range(2, len(level)-1):
                dot_data = level[i].split(".")
                dot_color = dot_data[0].replace("(", "").replace(")", "").split(",")
                dot_color = (int(dot_color[0]), int(dot_color[1]), int(dot_color[2]))
                dot_x = int(dot_data[1])
                dot_y = int(dot_data[2])

                new_dot = dot.EditorDot(dot_x, dot_y, dot_color, pack[level_num][0])
                pack[level_num].append(new_dot)

        level_number = 1
        editor_level_size = pack[level_number][0]
        interface.Text.texts["editor_level_text"].update_text(f"{level_number}")
        interface.Text.texts["editor_level_size_text"].update_text(f"{editor_level_size}x{editor_level_size}")

        Increase_Level()
        Decrease_Level()

# Runs every frame while the user is in the editor
def Draw() -> None:
    Convert_Mouse_To_Editor()
    grid.Draw_Border()
    Draw_Color_Picker()

    if not settings_open: # If settings page isn't open
        grid.Draw_Grid(editor_level_size)

        for dot_object in dot.EditorDot.dots:
            dot_object.draw()
    else: # If settings page is open
        pass