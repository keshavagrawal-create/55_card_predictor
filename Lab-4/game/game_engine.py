import pygame
from game.deck import Deck


class GameEngine:
    # Task 4: timing for the side-by-side reveal (milliseconds)
    SLIDE_MS = 300      # new card slides in from the right
    HOLD_MS = 1200      # both cards stay visible before the next round

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.deck = Deck()

        self.current_card = self.deck.draw()
        self.next_card = None
        self.score = 0
        self.status_msg = "Will the next card be HIGHER or LOWER?"
        self.status_color = (220, 220, 220)

        # Task 2: streak tracking
        self.streak = 0
        self.best_streak = 0
        self.last_points = 0

        # Task 4: reveal state
        self.revealing = False
        self.reveal_start = 0

        btn_w, btn_h = 140, 48
        self.btn_higher = pygame.Rect(width // 2 - btn_w - 20, height - 90, btn_w, btn_h)
        self.btn_lower = pygame.Rect(width // 2 + 20, height - 90, btn_w, btn_h)

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)

    # ------------------------------------------------------------------ #
    # Game logic
    # ------------------------------------------------------------------ #
    def get_multiplier(self, streak):
        """Task 2: 1x normally, 2x from 3 wins in a row, 3x from 5 in a row."""
        if streak >= 5:
            return 3
        if streak >= 3:
            return 2
        return 1

    def evaluate_guess(self, guess):
        """Draws next card and evaluates prediction."""
        self.next_card = self.deck.draw()

        new_rank = self.next_card.numeric_rank
        old_rank = self.current_card.numeric_rank
        vs_text = f"{self.next_card.rank_str} vs {self.current_card.rank_str}"

        # Task 3: tie / push -- score and streak are preserved
        if new_rank == old_rank:
            self.status_msg = f"PUSH / TIE! Rank matched. ({vs_text})"
            self.status_color = (255, 215, 0)
            self.start_reveal()
            return

        # Task 1: compare numeric ranks, not strings ("10" < "2" as strings!)
        if guess == "HIGHER":
            correct = new_rank > old_rank
        else:
            correct = new_rank < old_rank

        if correct:
            # Task 2: streak multiplier
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            mult = self.get_multiplier(self.streak)
            self.last_points = mult
            self.score += mult
            bonus = f"  +{mult} ({mult}x streak!)" if mult > 1 else "  +1"
            self.status_msg = f"CORRECT! {vs_text}{bonus}"
            self.status_color = (80, 220, 80)
        else:
            self.streak = 0
            self.score = max(0, self.score - 1)
            self.status_msg = f"WRONG! {vs_text}  Streak reset."
            self.status_color = (235, 75, 75)

        self.start_reveal()

    def start_reveal(self):
        """Task 4: show old + new card side by side before moving on."""
        self.revealing = True
        self.reveal_start = pygame.time.get_ticks()

    def finish_reveal(self):
        self.revealing = False
        self.current_card = self.next_card
        self.next_card = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignore clicks while the reveal is playing
            if self.revealing:
                return
            if self.btn_higher.collidepoint(event.pos):
                self.evaluate_guess("HIGHER")
            elif self.btn_lower.collidepoint(event.pos):
                self.evaluate_guess("LOWER")

    def update(self):
        if self.revealing:
            elapsed = pygame.time.get_ticks() - self.reveal_start
            if elapsed >= self.SLIDE_MS + self.HOLD_MS:
                self.finish_reveal()

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def draw_button(self, screen, rect, label, color):
        if self.revealing:
            color = tuple(c // 2 for c in color)  # dimmed while disabled
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), rect, width=2, border_radius=8)
        surf = self.font_medium.render(label, True, (255, 255, 255))
        screen.blit(surf, (rect.centerx - surf.get_width() // 2, rect.centery - surf.get_height() // 2))

    def render(self, screen):
        screen.fill((25, 80, 45))

        title_surf = self.font_title.render("High-Low Card Predictor", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 25))

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (30, 30))

        mult = self.get_multiplier(self.streak)
        streak_color = (255, 170, 60) if mult > 1 else (210, 210, 210)
        streak_surf = self.font_small.render(f"Streak: {self.streak}  ({mult}x)", True, streak_color)
        screen.blit(streak_surf, (30, 58))

        rem_surf = self.font_small.render(f"Deck: {self.deck.remaining} left", True, (210, 210, 210))
        screen.blit(rem_surf, (self.width - rem_surf.get_width() - 30, 35))

        best_surf = self.font_small.render(f"Best streak: {self.best_streak}", True, (210, 210, 210))
        screen.blit(best_surf, (self.width - best_surf.get_width() - 30, 58))

        card_w, card_h, card_y = 130, 180, 100

        if self.revealing and self.next_card is not None:
            # Task 4: previous card on the left, new card on the right
            left_x = self.width // 2 - card_w - 40
            right_x = self.width // 2 + 40

            elapsed = pygame.time.get_ticks() - self.reveal_start
            t = min(1.0, elapsed / self.SLIDE_MS)
            ease = 1 - (1 - t) ** 3  # ease-out
            slide_x = int(self.width + (right_x - self.width) * ease)

            self.current_card.render(screen, left_x, card_y, card_w, card_h)
            self.next_card.render(screen, slide_x, card_y, card_w, card_h)

            for text, x in (("Previous", left_x), ("New", right_x)):
                lbl = self.font_small.render(text, True, (230, 230, 230))
                screen.blit(lbl, (x + card_w // 2 - lbl.get_width() // 2, card_y - 22))

            vs = self.font_medium.render("vs", True, (245, 245, 245))
            screen.blit(vs, (self.width // 2 - vs.get_width() // 2, card_y + card_h // 2 - vs.get_height() // 2))
        else:
            self.current_card.render(screen, self.width // 2 - card_w // 2, card_y, card_w, card_h)

        status_surf = self.font_small.render(self.status_msg, True, self.status_color)
        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, 310))

        self.draw_button(screen, self.btn_higher, "HIGHER", (40, 140, 60))
        self.draw_button(screen, self.btn_lower, "LOWER", (170, 50, 50))
