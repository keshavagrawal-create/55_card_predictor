import pygame


class Card:

    def __init__(self, rank_str, suit_str, numeric_rank):
        self.rank_str = rank_str
        self.suit_str = suit_str
        self.numeric_rank = numeric_rank

        self.symbol = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}.get(suit_str, "")
        self.is_red = suit_str in ("Hearts", "Diamonds")
        self.color = (220, 40, 40) if self.is_red else (30, 30, 30)

    def render(self, surface, x, y, width=130, height=180):
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (255, 255, 255), card_rect, border_radius=10)
        pygame.draw.rect(surface, (50, 50, 50), card_rect, width=3, border_radius=10)

        font_rank = pygame.font.SysFont(None, 36)
        # Default font has no suit glyphs; try fonts that do (Mac / Windows / Linux)
        font_symbol = pygame.font.SysFont("applesymbols,segoeuisymbol,arialunicodems,dejavusans", 64)

        rank_surf = font_rank.render(self.rank_str, True, self.color)
        surface.blit(rank_surf, (x + 10, y + 8))

        symbol_surf = font_symbol.render(self.symbol, True, self.color)
        surface.blit(
            symbol_surf,
            (x + width // 2 - symbol_surf.get_width() // 2, y + height // 2 - symbol_surf.get_height() // 2),
        )

        surface.blit(rank_surf, (x + width - rank_surf.get_width() - 10, y + height - rank_surf.get_height() - 8))