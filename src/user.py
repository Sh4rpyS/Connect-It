import dot, game, grid, interface

class User:
    max_levels = 10
    loaded_level = 0
    loaded_pack = "NO PACK"

    def __init__(self, name: str) -> None:
        self.name = name
        self.highest_level = 0

    def Load_Data(self) -> None:
        pass

    def Save_Data(self) -> None:
        pass

    def Save_User(self) -> None:
        pass

def Load_User(self) -> None:
    # The user will be loaded here
    # Maybe multiple users at some point

    pass

def Clear_Level(level_size: int) -> None:
    game.level_size = level_size
    interface.Text.texts["level_size"].update_text(f"Level Size: {level_size}x{level_size}")

    grid.Tile.tiles.clear()
    grid.Tile.highlighted_tiles.clear()
    dot.Dot.dots.clear()

    grid.Tile.tiles = []
    grid.Tile.highlighted_tiles = []
    dot.Dot.dots = []
    grid.Tile.lines = {(255, 255, 255): []}

    # Create the tiles
    for i in range(game.level_size):
        for j in range(game.level_size):
            grid.Tile(25 + j * (550 / game.level_size), 125 + i * (550 / game.level_size))

def Load_Level(pack_name: str) -> None:
    interface.Button.buttons["continue"].set_active(False)
    with open(f"levels/{pack_name}.cpk", "r") as pack:
        pack = pack.read().replace("\n", "").split(":")
        User.max_levels = len(pack)

    pack_data = pack[User.loaded_level].split(";")
    level_size = pack_data[1]

    User.loaded_pack = pack_name

    interface.Text.texts["level_name"].update_text(f"{User.loaded_level+1}")
    interface.Text.texts["pack_name"].update_text(f"Pack: {User.loaded_pack}")
    interface.Text.texts["level_size"].update_text(f"Level Size: {game.level_size}x{game.level_size}")

    game.level_size = int(level_size)

    Clear_Level(game.level_size)

    for i in range(2, len(pack_data)-1):
        dot_data = pack_data[i].split(".")
        dot_color = dot_data[0].replace("(", "").replace(")", "").split(",")
        dot_color = (int(dot_color[0]), int(dot_color[1]), int(dot_color[2]))
        dot_x = int(dot_data[1])
        dot_y = int(dot_data[2])

        dot.Dot(25 + (550/game.level_size*dot_x), 125 + (550/game.level_size*dot_y), dot_color)