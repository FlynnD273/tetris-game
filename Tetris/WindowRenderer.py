from .RendererBase import RendererBase
from .Game import Game
from .Tile import Tile
from .Mino import OMino
import pygame

class WindowRenderer (RendererBase) :

    # Tile size: (width - 50)/15
    # Total width: (15x + 50)
    # Total Height: (20x + 30)
    def __init__(self, render_surface: pygame.Surface) :
        self.render_surface = render_surface
        self.tile_size = int((self.render_surface.get_width() - 50) / 15)
        self.background_color = "black"
        self.border_color = "white"
        self.preview_color = "grey"
        self.border_thickness = 5
        
    def render(self, game: Game) -> None:
        game_starting_point_x = (self.render_surface.get_width() - (15 * self.tile_size + 20)) / 2
        game_starting_point_y = 10

        top_border = pygame.Rect(game_starting_point_x - self.border_thickness, game_starting_point_y - self.border_thickness, self.tile_size * game.board.width + 2 * self.border_thickness, self.border_thickness)
        bot_border = pygame.Rect(game_starting_point_x - self.border_thickness, (game_starting_point_y) + self.tile_size * game.board.height, self.tile_size * game.board.width + 2 * self.border_thickness, self.border_thickness)
        lft_border = pygame.Rect(game_starting_point_x - self.border_thickness, game_starting_point_y, self.border_thickness, self.tile_size * game.board.height)
        rgt_border = pygame.Rect(game_starting_point_x + self.tile_size * game.board.width, game_starting_point_y, self.border_thickness, self.tile_size * game.board.height)

        scoring_width = self.tile_size * int(game.board.width / 2) + 2 * self.border_thickness
        scoring_starting_point_y = game_starting_point_y
        center = int((game_starting_point_x + self.tile_size * game.board.width + 10 + self.render_surface.get_width()) / 2)
        scoring_starting_point_x = center - int(scoring_width / 2)
        
        scoring_board_dimensions = 4

        preview_top_border = pygame.Rect(scoring_starting_point_x - self.border_thickness, scoring_starting_point_y - self.border_thickness, self.tile_size * int(game.board.width / 2) + 2 * self.border_thickness, self.border_thickness)
        preview_bot_border = pygame.Rect(scoring_starting_point_x - self.border_thickness, (scoring_starting_point_y) + self.tile_size * scoring_board_dimensions, self.tile_size * int(game.board.width / 2) + 2 * self.border_thickness, self.border_thickness)
        preview_rgt_border = pygame.Rect(scoring_starting_point_x + self.tile_size * int(game.board.width / 2), scoring_starting_point_y, self.border_thickness, self.tile_size * scoring_board_dimensions)
        preview_lft_border = pygame.Rect(scoring_starting_point_x - self.border_thickness, scoring_starting_point_y, self.border_thickness, self.tile_size * scoring_board_dimensions)
        
        scoring_top_border = pygame.Rect((preview_top_border.x, preview_bot_border.y + 10), (preview_top_border.width, preview_top_border.height))
        scoring_bot_border = pygame.Rect((preview_bot_border.x, preview_bot_border.y + self.tile_size * scoring_board_dimensions + 10), (preview_bot_border.width, preview_bot_border.height))
        scoring_lft_border = pygame.Rect((preview_lft_border.x, preview_bot_border.y + 10), (preview_lft_border.width, preview_lft_border.height))
        scoring_rgt_border = pygame.Rect((preview_rgt_border.x, preview_bot_border.y + 10), (preview_rgt_border.width, preview_rgt_border.height))
        
        # Clear the background
        self.render_surface.fill(self.getColor(Tile.Clear))

        tile = game.nextPiece
        for row in range(4) :
            for col in range(4) :
                # Center the tile
                if tile.color == Tile.Yellow :
                    offset_x = 0.5
                    offset_y = 1
                elif tile.color != Tile.LBlue :
                    offset_x = 1
                    offset_y = 0
                else :
                    offset_x = 0.5
                    offset_y = -0.5

                self.render_surface.fill(self.getColor(tile.getTile(row, col)), pygame.Rect(scoring_starting_point_x + ((col + offset_x) * self.tile_size), scoring_starting_point_y + ((row + offset_y) * self.tile_size), self.tile_size, self.tile_size))

        # Fill in border lines
        self.render_surface.fill(self.border_color, top_border)
        self.render_surface.fill(self.border_color, bot_border)
        self.render_surface.fill(self.border_color, lft_border)
        self.render_surface.fill(self.border_color, rgt_border)

        self.render_surface.fill(self.border_color, preview_top_border)
        self.render_surface.fill(self.border_color, preview_bot_border)
        self.render_surface.fill(self.border_color, preview_lft_border)
        self.render_surface.fill(self.border_color, preview_rgt_border)

        self.render_surface.fill(self.border_color, scoring_top_border)
        self.render_surface.fill(self.border_color, scoring_bot_border)
        self.render_surface.fill(self.border_color, scoring_lft_border)
        self.render_surface.fill(self.border_color, scoring_rgt_border)
        # Text 
        font = pygame.font.Font('freesansbold.ttf', int((22/25) * self.tile_size))
        
        score = font.render(f'Score: ', True, self.border_color, self.background_color)
        score_value = font.render(f'{game.score}', True, self.border_color, self.background_color)
        level = font.render(f'Level: ', True, self.border_color, self.background_color)
        level_value = font.render(f'{game.level}', True, self.border_color, self.background_color)

        score_rect: pygame.Rect = score.get_rect()
        score_value_rect: pygame.Rect = score_value.get_rect()
        level_rect: pygame.Rect = level.get_rect()
        level_value_rect: pygame.Rect = level_value.get_rect()
        
        score_rect.centerx = (int(scoring_top_border.topright[0]  + scoring_top_border.topleft[0])/2)
        score_rect.y = scoring_top_border.bottomright[1] + 5
        score_value_rect.topleft = score_rect.bottomleft
        level_rect.topleft = score_value_rect.bottomleft
        level_value_rect.topleft = level_rect.bottomleft

        # Printing the text to the surface is a bit odd
        self.render_surface.blit(score, score_rect)
        self.render_surface.blit(score_value, score_value_rect)
        self.render_surface.blit(level, level_rect)
        self.render_surface.blit(level_value, level_value_rect)
        
        # I stole this, thank you
        ghost = game.piece.copy()
        offRow, offCol = ghost.offset
        ghost.offset = (offRow + game.piece.distToGround(game.board), offCol)
        for row in range(game.board.height) :
            for col in range(game.board.width) :
                tile = game.piece.getTileWithOffset(row, col)
                if tile == Tile.Clear:
                    tile = ghost.getTileWithOffset(row, col)
                    if tile == Tile.Clear:
                        tile = game.board.getTile(row, col)
                    else:
                        self.render_surface.fill(self.preview_color, pygame.Rect(game_starting_point_x + (col * self.tile_size), game_starting_point_y + (row * self.tile_size), self.tile_size, self.tile_size))
                        continue
                self.render_surface.fill(self.getColor(tile), pygame.Rect(game_starting_point_x + (col * self.tile_size), game_starting_point_y + (row * self.tile_size), self.tile_size, self.tile_size))

        # Update the surface
        pygame.display.flip()
    
    def getColor(self, tile: Tile) -> str:
        """Map a Tile color to the pygame-safe color"""
        color = self.background_color
        match tile:
            case Tile.LBlue:
                color = "cyan"
            case Tile.DBlue:
                color = "blue"
            case Tile.Orange:
                color = "orange"
            case Tile.Yellow:
                color = "yellow"
            case Tile.Green:
                color = "green"
            case Tile.Red:
                color = "red"
            case Tile.Magenta:
                color = "magenta"

        return color

def build_screen_and_render_from_height(width: int) -> (pygame.Surface, WindowRenderer) :
    """Setup window and the renderer in one go."""
    screen = pygame.display.set_mode((width, (20 * int((width - 50) / 15)) + 20))
    renderer = WindowRenderer(screen)

    return (screen, renderer)

if __name__ == "__main__" :
    # For testing purposes
    pass