import pygame, sys, grid, dot, interface, win32gui, win32con, user, levels, editor
from pygame.locals import *

pygame.init()

def Init(fps: int, console: bool) -> None: # Initializes game window etc
    global screen, clock, screen_width, screen_height, scene, fps_max

    fps_max = fps
    screen_width = 600
    screen_height = 700

    scene = "menu" # "menu", "game", "editor"

    if not console:
        hide = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hide , win32con.SW_HIDE)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption("CONNECT IT")

    game_icon = pygame.image.load("res/image.png")
    pygame.display.set_icon(game_icon)
    pygame.key.set_repeat(300, 35)

def Start_Game() -> None: # Starts the game
    Start()

    while 1: # Game loop
        Update()

def End_Game() -> None:
    pygame.quit()
    sys.exit()

def Start() -> None: # Run once when the game is started, can be used to create objects
    global level_size, dot_collision, dot_target, pack_page, level_page

    dot_collision = False
    dot_target = None

    level_size = 5
    pack_page = 1
    level_page = 1

    # Initialize main menu UI objects
    interface.Text("title", "menu", 300, 200, "CONNECT IT", 52, alignment="center")
    interface.Text("version", "menu", 6, 675, "Version 0.7.1", 18, alignment="none")
    interface.Text("dev", "menu", 594, 650, "Made By Veeti Tuomola (C)", 18, alignment="right")
    interface.Text("creds", "menu", 594, 675, "Made with Python 3.10.2 & Pygame 2.1.2", 18, alignment="right")
    
    interface.Button("play", "menu", 300, 300, 200, 60, "PLAY", 32, text_alignment="center", button_alignemnt="center")
    interface.Button("editor", "menu", 300, 380, 200, 60, "EDITOR", 32, text_alignment="center", button_alignemnt="center")
    interface.Button("exit", "menu", 300, 460, 200, 60, "EXIT", 32, text_alignment="center", button_alignemnt="center")
    
    # Initialize game UI objects
    interface.Text("pack_name", "game", 130, 17, f"Pack: {user.User.loaded_pack}", 24, alignment="none")
    interface.Text("level_size", "game", 130, 47, f"Level Size: {level_size}x{level_size}", 24, alignment="none")
    interface.Text("completion", "game", 130, 77, f"Completion: 0%", 24, alignment="none")

    interface.Text("level_name", "game", 67, 59, f"{user.User.loaded_level}", 42, alignment="center")
    
    interface.Button("game_to_menu", "game", 517, 33, 125, 40, "MENU", 28, text_alignment="center", button_alignemnt="center")
    interface.Button("game_to_levels", "game", 517, 86, 125, 40, "LEVELS", 28, text_alignment="center", button_alignemnt="center")

    interface.Button("continue", "game", 300, 380, 255, 80, "NEXT LEVEL", 32, text_alignment="center", button_alignemnt="center")
    interface.Button.buttons["continue"].set_active(False)

    # Initializes other scenes when the game launches
    levels.Init()
    grid.Init()
    editor.Init()

def Get_Input() -> None:
    global mouse_pos, mouse_press, dot_collision, scene, level_size, dot_target

    # Gets user input, mouse position and press for example
    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()

    # Gets pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            End_Game()
        if event.type == pygame.MOUSEBUTTONUP:
            if scene == "game":
                if grid.completion == 100:
                    interface.Button.buttons["continue"].set_active(True)
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Go through the buttons and if an event is happening, do its event
            interface.Button_Functionality()
            
            # Scene specific events
            if scene == "game":
                # If mouse if over a DOT, then start highlighting
                for dot_object in dot.Dot.dots:
                    if dot_object.collider_obj.collidepoint(mouse_pos):
                        dot_target = dot_object
                        grid.Tile.lines[dot_object.color].clear()
                        dot_collision = True
                        break
                    else:
                        dot_collision = False
            elif scene == "editor" and not editor.settings_open:
                editor.Create_New_Dot()
        if event.type == pygame.KEYDOWN and interface.InputBox.targeted != "":
            interface.Input_Box_Functionality(event.key, event.mod)

def Count_Delta_Time() -> None:
    global delta_time, ticks, get_ticks_last_frame

    if not "get_ticks_last_frame" in globals():
        get_ticks_last_frame = pygame.time.get_ticks()

    ticks = pygame.time.get_ticks()
    delta_time = (ticks - get_ticks_last_frame) / 1000.0
    get_ticks_last_frame = ticks

def Update() -> None: # Update function, will be inside a while True loop
    Get_Input()
    Count_Delta_Time()

    Draw()
    pygame.display.update()
    
    clock.tick(fps_max) # Used to limit fps
    pygame.display.set_caption(f"CONNECT IT {int(clock.get_fps())} FPS")

def Draw() -> None: # Draws everything
    screen.fill((0, 0, 0))

    # Draws the objects depending on the scene
    if scene == "levels": Draw_Levels()
    elif scene == "game": Draw_Game()
    elif scene == "editor": Draw_Editor()

    interface.Draw() # Draws all the UI objects

# Draws the menu for the level selection
def Draw_Levels() -> None:
    levels.Draw()

# Draws the enviroment for the main game view
def Draw_Game() -> None:
    pygame.draw.rect(screen, (255, 255, 255), (21, 13, 92, 92), width = 4)
    grid.Draw() # Draws the grid for the game view
    dot.Draw() # Draws the DOTS on the screen (the ones that you need to connect)

# Draws the enviroment for the editor view
def Draw_Editor() -> None:
    editor.Draw() # Draws the editor specific stuff