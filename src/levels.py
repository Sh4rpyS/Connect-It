import pygame, game, os, interface

# Runs once when the game is opened
def Init() -> None:
    global level_packs, pack_buttons, highlight, selected_index, level_name

    # Initialize level selection UI objects
    interface.Text("levels_header", "levels", 300, 65, "LEVEL SELECTION", 52, alignment="center")
    interface.Text("page", "levels", 300, 590, f"PAGE {game.pack_page}", 24, alignment="center")
    
    interface.Button("page_down", "levels", 158, 590, 100, 40, "<", 32, text_alignment="center", button_alignemnt="center")
    interface.Button("page_up", "levels", 442, 590, 100, 40, ">", 32, text_alignment="center", button_alignemnt="center")
    interface.Button("levels_back", "levels", 158, 650, 274, 60, "BACK TO MENU", 32, text_alignment="center", button_alignemnt="center")
    interface.Button("levels_play", "levels", 442, 650, 274, 60, "OPEN PACK", 32, text_alignment="center", button_alignemnt="center")

    pack_buttons = []

    level_packs = os.listdir("levels")
    viable_level_packs = []
    level_name = ""

    # Sort out the not proper level files
    for pack in level_packs:
        try:
            pack_ = str(pack).split(".")
            if pack_[1] == "cpk": viable_level_packs.append(pack)
        except: pass
    level_packs = viable_level_packs[:]

    selected_index = 10

    highlight = pygame.Surface((540, 84))
    highlight.fill((255, 255, 255))

    # Create the buttons, and add them to a list of their own
    for i in range(5):
        pack_button = interface.Button(f"level_{i}", "levels", 35, 135+(84*i), 530, 74, "LEVEL NAME HERE", 32, text_alignment="none", button_alignemnt="none")
        interface.Text.texts[f"level_{i}_button"].active = False
        interface.Button.buttons[f"level_{i}"].active = False
        pack_buttons.append(pack_button)

    Update_Page()

def Update_Page() -> None:
    # Hides all the buttons
    for i in range(5):
        interface.Button.buttons[f"level_{i}"].set_active(False)

    if len(level_packs) - (game.pack_page-1)*5 > 5: loop = 5
    else: loop = len(level_packs) - (game.pack_page-1)*5

    for i in range(loop):
        # Get the pack name
        pack_name = str(level_packs[i+((game.pack_page-1)*5)]).split(".")[0]

        # Makes some buttons visible, depending on the situation, and updates them
        interface.Button.buttons[f"level_{i}"].set_active(True)
        interface.Text.texts[f"level_{i}_button"].update_text(pack_name)

def Page_Up() -> None:
    global selected_index

    if game.pack_page < len(level_packs)/5:
        game.pack_page += 1
        selected_index = 10
        interface.Text.texts["page"].update_text(f"PAGE {game.pack_page}")

        Update_Page()

def Page_Down() -> None:
    global selected_index

    if game.pack_page > 1:
        game.pack_page -= 1
        selected_index = 10
        interface.Text.texts["page"].update_text(f"PAGE {game.pack_page}")

        Update_Page()

# Runs every frame while the user is in the level selection menu
def Draw() -> None:
    global level_name

    # Draw the border for the level menu
    pygame.draw.rect(game.screen, (255, 255, 255), (21, 121, 558, 438), width = 4)

    if selected_index != 10: level_name = str(level_packs[selected_index+((game.pack_page-1)*5)]).split(".")[0]
    else: level_name = ""

    game.screen.blit(highlight, (30, 130+(84*selected_index)))