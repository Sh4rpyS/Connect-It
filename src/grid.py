import pygame, game, dot, interface

class Tile:
    tiles = []
    highlighted_tiles = []

    lines = {(255, 255, 255): []}

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.alpha = 0
        self.highlighted_alpha = 100
        self.max_highlight = 50
        self.size = 550 / game.level_size
        self.color = (255, 255, 255)
        self.alpha_color = (0, 0, 0)
        self.highlighted_color = (255, 255, 255)

        self.object = pygame.Surface((self.size, self.size))
        self.object.fill(self.color)

        collider = pygame.Surface((self.size, self.size))

        h_collider = pygame.Surface((self.size * 1.2, self.size / 2))
        v_collider = pygame.Surface((self.size / 2, self.size * 1.2))

        self.collider_object = game.screen.blit(collider, (self.x, self.y))
        self.h_coll_obj = game.screen.blit(h_collider, (self.x, self.y + (self.size * 1.2) / 4))
        self.v_coll_obj = game.screen.blit(v_collider, (self.x + (self.size * 1.2) / 4, self.y))
        
        Tile.tiles.append(self)

    # Converts colors to act like they have alpha values
    def convert_alpha(color: tuple, alpha: float) -> tuple:
        r = int(color[0] * (alpha/255))
        g = int(color[1] * (alpha/255))
        b = int(color[2] * (alpha/255))

        return (r, g, b)

    def add_to_highlight(target) -> None:
        wrong_dot_collision = False
        for dot_object in dot.Dot.dots:
            if dot_object.collider_obj.collidepoint(game.mouse_pos) and dot_object.color != game.dot_target.color:
                wrong_dot_collision = True
                break
        
        if not wrong_dot_collision:
            target.highlighted_color = game.dot_target.color
            target.alpha = target.max_highlight
            Tile.highlighted_tiles.append(target)

            Count_Level_Completion()
        else:
            Tile.highlighted_tiles.clear()
            Count_Level_Completion()
            game.dot_collision = False

    def draw(self) -> None:
        if self.collider_object.collidepoint(game.mouse_pos): # Highlight the tile if you hover over it
            # If left mouse button is held start creating the path  
            if game.dot_collision and game.mouse_press[0]:
                if not self in Tile.highlighted_tiles and len(Tile.highlighted_tiles) > 0:
                    # Declare the variables to keep the if statements cleaner
                    last_v_coll = Tile.highlighted_tiles[-1].v_coll_obj
                    last_h_coll = Tile.highlighted_tiles[-1].h_coll_obj
                    v_coll = self.v_coll_obj
                    h_coll = self.h_coll_obj

                    # Check if the tile is touching another tile
                    if v_coll.colliderect(last_v_coll) or h_coll.colliderect(last_h_coll):
                        Tile.add_to_highlight(self)

                    # This happens if it isn't touching
                    else:
                        corner_block_found = True

                        try:
                            # Get the index of the block
                            self_index = Tile.tiles.index(self)

                            # Get objects around the blocks
                            u = Tile.tiles[self_index-game.level_size]
                            r = Tile.tiles[self_index+1]
                            b = Tile.tiles[self_index+game.level_size]
                            l = Tile.tiles[self_index-1]

                            # Check if any of the blocks are touching
                            if u.v_coll_obj.colliderect(last_v_coll) or u.h_coll_obj.colliderect(last_h_coll): Tile.add_to_highlight(u)
                            elif r.v_coll_obj.colliderect(last_v_coll) or r.h_coll_obj.colliderect(last_h_coll): Tile.add_to_highlight(r)
                            elif b.v_coll_obj.colliderect(last_v_coll) or b.h_coll_obj.colliderect(last_h_coll): Tile.add_to_highlight(b)
                            elif l.v_coll_obj.colliderect(last_v_coll) or l.h_coll_obj.colliderect(last_h_coll): Tile.add_to_highlight(l)
                            else: corner_block_found = False
                        except: # This is just to ignore possible index errors
                            pass

                        # Check if it is possible to create an extra block to make it connect
                        if corner_block_found:
                            Tile.add_to_highlight(self)

                        # If it isn't possible, cut the line
                        else:
                            Tile.highlighted_tiles.clear()
                            Count_Level_Completion()
                            game.dot_collision = False
                else:
                    # Add the tile to the start, this should only happen once
                    if not self in Tile.highlighted_tiles:
                        Tile.add_to_highlight(self)

                    # Allows going backwards and cutting lines
                    else:
                        for index, tile in enumerate(Tile.highlighted_tiles):
                            if tile.collider_object.collidepoint(game.mouse_pos):
                                # Cuts the line
                                Tile.highlighted_tiles = Tile.highlighted_tiles[0:index+1]
                                Count_Level_Completion()
                                break

                if self.color != (255, 255, 255):
                    Tile.lines[self.color].clear()

            elif not self in Tile.highlighted_tiles and not self in Tile.lines[self.highlighted_color]:
                # Highlight the tile
                self.alpha = self.max_highlight

            # Stop creating the line
            if not game.mouse_press[0] and len(Tile.highlighted_tiles) > 0:
                for dot_object in dot.Dot.dots:
                    # Checks if the line is done
                    if dot_object.collider_obj.collidepoint(game.mouse_pos) and dot_object.color == game.dot_target.color and not dot_object == game.dot_target:
                        # Create the line
                        Tile.lines[game.dot_target.color] = Tile.highlighted_tiles[:]

                Tile.highlighted_tiles.clear()
                Count_Level_Completion()
                game.dot_collision = False

        # Fade the tile if it isn't line highlighted
        elif self.alpha > 0 and not self in Tile.highlighted_tiles and not self in Tile.lines[self.highlighted_color]:
            self.alpha -= 200 * game.delta_time
            if self.alpha < 0: self.alpha = 0


        # Don't draw if the alpha is 0
        if self.alpha > 0:
            alpha_color = Tile.convert_alpha(self.color, self.alpha)

            if self in Tile.highlighted_tiles:
                self.alpha = self.highlighted_alpha
                # Set the color for the line to be same as the dot
                if self.color != game.dot_target.color:
                    self.color = game.dot_target.color
                    self.alpha_color = alpha_color
                    self.object.fill(self.alpha_color)
                elif self.alpha_color != alpha_color:
                    self.alpha_color = alpha_color
                    self.object.fill(self.alpha_color)
            
            # Color the tiles for the correct color depending on the dots
            elif self.highlighted_color in Tile.lines.keys() and self in Tile.lines[self.highlighted_color]:
                if self.color != self.highlighted_color:
                    self.color = self.highlighted_color
                    self.alpha_color = Tile.convert_alpha(self.color, self.alpha)
                    self.object.fill(self.alpha_color)

            else:
                # Reset the color back to white
                if self.color != (255, 255, 255):
                    self.color = (255, 255, 255)
                    self.alpha_color = alpha_color
                    self.object.fill(self.alpha_color)
                elif self.alpha_color != alpha_color:
                    self.alpha_color = alpha_color
                    self.object.fill(self.alpha_color)
            
            game.screen.blit(self.object, (self.x, self.y))

def Init() -> None:    
    global vertical_line, horizontal_line, border, completion

    # Create the lines for the grid
    vertical_line = pygame.Surface((1, 550))
    vertical_line.fill((200, 200, 200))
    horizontal_line = pygame.Surface((550, 1))
    horizontal_line.fill((200, 200, 200))

    # Create the border for the grid
    border = pygame.Surface((558, 558))

    horizontal = pygame.Surface((558, 4))
    horizontal.fill((255, 255, 255))

    border.blit(horizontal, (0, 0))
    border.blit(horizontal, (0, 554))

    vertical = pygame.Surface((4, 558))
    vertical.fill((255, 255, 255))

    border.blit(vertical, (0, 0))
    border.blit(vertical, (554, 0))

    completion = 0

def Count_Level_Completion() -> None:
    global completion

    painted_tiles = 0

    for line in Tile.lines.values():
        painted_tiles += len(line)

    painted_tiles += len(Tile.highlighted_tiles)
        
    completion = int(painted_tiles / len(Tile.tiles) * 100)
    interface.Text.texts["completion"].update_text(f"Completion: {completion}%")

def Draw_Border() -> None:
    # Border for the game area
    game.screen.blit(border, (21, 121))

def Draw_Tiles() -> None:
    for tile in Tile.tiles:
        tile.draw()

def Draw_Grid(size: int) -> None:
    for i in range(1, size):
        # Draw vertical lines
        x = 25 + (i * (550 / size))
        game.screen.blit(vertical_line, (x, 125))

        # Draw horizontal lines
        y = 125 + (i * (550 / size))
        game.screen.blit(horizontal_line, (25, y))

def Draw() -> None:
    Draw_Border()
    Draw_Tiles()
    Draw_Grid(game.level_size)