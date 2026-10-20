"""Pastel Sudoku, a mouse-and-keyboard Sudoku game built with pygame."""

from __future__ import annotations

import time

import pygame

from sudoku import DIFFICULTIES, SudokuBoard, SudokuGenerator

WIDTH, HEIGHT = 1000, 760
BOARD_X, BOARD_Y, CELL = 56, 176, 60
BOARD_SIZE = CELL * 9

COLORS = {
    "background": (253, 249, 245),
    "white": (255, 255, 255),
    "ink": (65, 68, 81),
    "muted": (132, 133, 143),
    "lavender": (240, 217, 239),
    "pink": (252, 220, 225),
    "yellow": (255, 230, 187),
    "sage": (233, 236, 206),
    "mint": (205, 233, 220),
    "blue": (196, 223, 229),
    "line": (221, 218, 217),
    "strong_line": (153, 155, 166),
    "selected": (255, 237, 194),
    "related": (250, 245, 230),
    "wrong": (255, 222, 225),
    "accent": (145, 117, 168),
    "success": (81, 145, 116),
    "border": (235, 231, 229),
    "lavender_dark": (126, 100, 149),
}


class SudokuGame:
    """Own the pygame window, screens, input and drawing."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Sudoku de Nubes")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_family = "segoeui"
        self.font = pygame.font.SysFont(self.font_family, 20)
        self.small_font = pygame.font.SysFont(self.font_family, 16)
        self.medium_font = pygame.font.SysFont(self.font_family, 26, bold=True)
        self.title_font = pygame.font.SysFont(self.font_family, 40, bold=True)
        self.digit_font = pygame.font.SysFont("bahnschrift", 34, bold=True)
        self.screen_name = "menu"
        self.board: SudokuBoard | None = None
        self.difficulty = "Fácil"
        self.selected: tuple[int, int] | None = None
        self.notes_mode = False
        self.started_at = time.monotonic()
        self.message = ""
        self.message_until = 0.0
        self.buttons: dict[str, pygame.Rect] = {}
        self.running = True

    def start_game(self, difficulty: str) -> None:
        puzzle, solution = SudokuGenerator.generate(difficulty)
        self.board = SudokuBoard(puzzle, solution)
        self.difficulty = difficulty
        self.selected = None
        self.notes_mode = False
        self.started_at = time.monotonic()
        self.screen_name = "game"

    def notify(self, message: str) -> None:
        self.message = message
        self.message_until = time.monotonic() + 2.2

    def run(self) -> None:
        while self.running:
            self._events()
            self._draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def _events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._key_down(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._mouse_down(event.pos)

    def _key_down(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            if self.screen_name == "game":
                self.screen_name = "menu"
            else:
                self.running = False
            return
        if self.screen_name != "game" or self.board is None:
            return
        if event.key in (pygame.K_n,):
            self.notes_mode = not self.notes_mode
        elif event.key == pygame.K_h:
            self._hint()
        elif event.key == pygame.K_r:
            self.start_game(self.difficulty)
        elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_0, pygame.K_KP0):
            if self.selected:
                self.board.clear(*self.selected)
        elif pygame.K_1 <= event.key <= pygame.K_9:
            self._enter_value(event.key - pygame.K_0)
        elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
            self._enter_value(event.key - pygame.K_KP0)
        elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            self._move_selection(event.key)

    def _enter_value(self, value: int) -> None:
        if self.board is None or self.selected is None:
            return
        self.board.set_value(*self.selected, value, notes_mode=self.notes_mode)
        if self.board.values[self.selected[0]][self.selected[1]] == value:
            if value != self.board.solution[self.selected[0]][self.selected[1]] and not self.notes_mode:
                self.notify("Ese número no va aquí. ¡Inténtalo de nuevo!")
            elif self.board.is_complete():
                self.notify("¡Sudoku resuelto! ¡Qué genial!")

    def _move_selection(self, key: int) -> None:
        row, col = self.selected or (0, 0)
        if key == pygame.K_UP:
            row = (row - 1) % 9
        elif key == pygame.K_DOWN:
            row = (row + 1) % 9
        elif key == pygame.K_LEFT:
            col = (col - 1) % 9
        else:
            col = (col + 1) % 9
        self.selected = row, col

    def _hint(self) -> None:
        if self.board is None or self.selected is None:
            self.notify("Selecciona una casilla vacía primero.")
        elif self.board.hint(*self.selected):
            self.notify("¡Pista colocada!")
            if self.board.is_complete():
                self.notify("¡Sudoku resuelto! ¡Qué genial!")
        else:
            self.notify("Esa casilla ya está resuelta o es una pista.")

    def _mouse_down(self, position: tuple[int, int]) -> None:
        x, y = position
        if self.screen_name == "menu":
            for difficulty in DIFFICULTIES:
                if self.buttons.get(difficulty, pygame.Rect(0, 0, 0, 0)).collidepoint(position):
                    self.start_game(difficulty)
                    return
            return

        if BOARD_X <= x < BOARD_X + BOARD_SIZE and BOARD_Y <= y < BOARD_Y + BOARD_SIZE:
            self.selected = ((y - BOARD_Y) // CELL, (x - BOARD_X) // CELL)
            return
        for name, rect in self.buttons.items():
            if rect.collidepoint(position):
                if name == "pista":
                    self._hint()
                elif name == "notas":
                    self.notes_mode = not self.notes_mode
                elif name == "nuevo":
                    self.start_game(self.difficulty)
                elif name == "menu":
                    self.screen_name = "menu"
                return

    def _draw(self) -> None:
        self.screen.fill(COLORS["background"])
        if self.screen_name == "menu":
            self._draw_menu()
        else:
            self._draw_game()
        if self.message and time.monotonic() < self.message_until:
            self._draw_toast(self.message)

    def _draw_menu(self) -> None:
        self._draw_decorations()
        self._draw_icon("grid", (WIDTH // 2 - 120, 107), COLORS["accent"], 30)
        self._text("SUDOKU", self.title_font, COLORS["ink"], (WIDTH // 2, 107), center=True)
        self._text(
            "Un momento de calma, color y números",
            self.font,
            COLORS["muted"],
            (WIDTH // 2, 157),
            center=True,
        )
        self._rounded((190, 205, 620, 405), COLORS["white"], 28, shadow=True)
        self._text("Elige tu nivel", self.medium_font, COLORS["ink"], (WIDTH // 2, 251), center=True)
        self._text("Cada tablero tiene una solución única", self.small_font, COLORS["muted"],
                   (WIDTH // 2, 282), center=True)
        self.buttons = {}
        cards = [
            ("Fácil", COLORS["mint"], "Para empezar", "easy"),
            ("Intermedio", COLORS["yellow"], "Un buen reto", "medium"),
            ("Difícil", COLORS["pink"], "¡A por todas!", "hard"),
        ]
        for index, (name, color, subtitle, icon) in enumerate(cards):
            rect = pygame.Rect(220 + index * 188, 314, 168, 178)
            self.buttons[name] = rect
            self._rounded(rect, color, 20)
            self._draw_icon(icon, (rect.centerx, 350), COLORS["ink"], 24)
            self._text(name, self.medium_font, COLORS["ink"], (rect.centerx, 390), center=True,
                       max_width=rect.width - 16)
            self._text(subtitle, self.small_font, COLORS["muted"], (rect.centerx, 422), center=True,
                       max_width=rect.width - 16)
            self._text(f"{81 - DIFFICULTIES[name]} casillas dadas", self.small_font, COLORS["ink"],
                       (rect.centerx, 464), center=True, max_width=rect.width - 16)
        self._draw_icon("pointer", (WIDTH // 2 - 151, 544), COLORS["accent"], 16)
        self._text("Haz clic en una tarjeta para comenzar", self.small_font, COLORS["muted"],
                   (WIDTH // 2 + 8, 544), center=True)
        self._text("Tómate tu tiempo. ¡Disfruta cada número!", self.small_font, COLORS["accent"],
                   (WIDTH // 2, 695), center=True)

    def _draw_game(self) -> None:
        self._draw_decorations()
        self._draw_icon("grid", (72, 76), COLORS["accent"], 27)
        self._text("SUDOKU", self.title_font, COLORS["ink"], (98, 53))
        self._text("de Nubes", self.font, COLORS["accent"], (274, 70))
        self._rounded((58, 116, 145, 31), COLORS["lavender"], 12)
        self._text(f"Nivel {self.difficulty.lower()}", self.small_font, COLORS["lavender_dark"],
                   (71, 122), max_width=120)
        self._text("Selecciona una casilla y escribe del 1 al 9", self.small_font, COLORS["muted"],
                   (BOARD_X, 151), max_width=BOARD_SIZE)
        self._draw_board()
        self._draw_panel()
        if self.board and self.board.is_complete():
            self._draw_win_overlay()

    def _draw_board(self) -> None:
        assert self.board is not None
        rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)
        self._rounded(rect.inflate(12, 12), COLORS["white"], 17, shadow=True)
        conflicts = self.board.conflicts()
        incorrect = {
            (row, col)
            for row in range(9)
            for col in range(9)
            if self.board.values[row][col]
            and self.board.values[row][col] != self.board.solution[row][col]
        }
        selected = self.selected
        selected_value = self.board.values[selected[0]][selected[1]] if selected else 0
        for row in range(9):
            for col in range(9):
                cell_rect = pygame.Rect(BOARD_X + col * CELL, BOARD_Y + row * CELL, CELL, CELL)
                color = COLORS["white"]
                if selected and (row == selected[0] or col == selected[1]):
                    color = COLORS["related"]
                if selected and row // 3 == selected[0] // 3 and col // 3 == selected[1] // 3:
                    color = COLORS["related"]
                if selected and (row, col) == selected:
                    color = COLORS["selected"]
                if (row, col) in conflicts or (row, col) in incorrect:
                    color = COLORS["wrong"]
                pygame.draw.rect(self.screen, color, cell_rect)
                value = self.board.values[row][col]
                if value:
                    is_given = (row, col) in self.board.givens
                    is_match = selected_value != 0 and value == selected_value
                    text_color = COLORS["ink"] if is_given else COLORS["accent"]
                    if is_match:
                        text_color = COLORS["success"]
                    self._text(str(value), self.digit_font, text_color, cell_rect.center, center=True)
                else:
                    notes = self.board.notes.get((row, col), set())
                    for note in notes:
                        note_rect = pygame.Rect(
                            cell_rect.x + ((note - 1) % 3) * 20,
                            cell_rect.y + ((note - 1) // 3) * 19,
                            20,
                            19,
                        )
                        self._text(str(note), self.small_font, COLORS["muted"], note_rect.center,
                                   center=True)

        for index in range(10):
            width = 3 if index % 3 == 0 else 1
            color = COLORS["strong_line"] if index % 3 == 0 else COLORS["line"]
            pygame.draw.line(
                self.screen, color, (BOARD_X + index * CELL, BOARD_Y),
                (BOARD_X + index * CELL, BOARD_Y + BOARD_SIZE), width,
            )
            pygame.draw.line(
                self.screen, color, (BOARD_X, BOARD_Y + index * CELL),
                (BOARD_X + BOARD_SIZE, BOARD_Y + index * CELL), width,
            )

    def _draw_panel(self) -> None:
        assert self.board is not None
        panel = pygame.Rect(624, 176, 320, 540)
        self._rounded(panel, COLORS["white"], 24, shadow=True)
        self._draw_icon("sparkle", (674, 207), COLORS["accent"], 18)
        self._text("Tu partida", self.medium_font, COLORS["ink"], (692, 192))
        self._text(self.difficulty, self.small_font, COLORS["lavender_dark"], (902, 203),
                   center=True, max_width=74)
        elapsed = int(time.monotonic() - self.started_at)
        self._rounded((648, 238, 272, 72), COLORS["lavender"], 16)
        self._draw_icon("clock", (681, 274), COLORS["lavender_dark"], 22)
        self._text("TIEMPO", self.small_font, COLORS["muted"], (711, 248))
        self._text(f"{elapsed // 60:02d}:{elapsed % 60:02d}", self.medium_font, COLORS["ink"],
                   (711, 267))

        self.buttons = {}
        self._draw_stat_card("Errores", str(self.board.mistakes),
                             pygame.Rect(648, 322, 130, 65), COLORS["pink"])
        self._draw_stat_card("Pistas usadas", str(self.board.hints_used),
                             pygame.Rect(790, 322, 130, 65), COLORS["yellow"])
        self._draw_button("pista", "Dame una pista", pygame.Rect(648, 402, 272, 50),
                          COLORS["mint"], icon="bulb")
        note_color = COLORS["yellow"] if self.notes_mode else COLORS["sage"]
        self._draw_button(
            "notas",
            f"Notas: {'activadas' if self.notes_mode else 'desactivadas'}",
            pygame.Rect(648, 463, 272, 48),
            note_color,
            icon="pencil",
        )
        self._draw_button("nuevo", "Nuevo", pygame.Rect(648, 522, 130, 46), COLORS["blue"],
                          icon="refresh")
        self._draw_button("menu", "Menú", pygame.Rect(790, 522, 130, 46), COLORS["pink"],
                          icon="home")
        self._rounded((648, 580, 272, 124), (250, 248, 246), 16)
        self._text("ATAJOS", self.small_font, COLORS["muted"], (666, 584))
        self._draw_key_hint("1–9", "Escribir número", (666, 608))
        self._draw_key_hint("Supr", "Borrar casilla", (666, 630))
        self._draw_key_hint("N · H · R", "Notas · pista · reiniciar", (666, 652))
        self._draw_key_hint("Esc", "Volver al menú", (666, 674))

    def _draw_win_overlay(self) -> None:
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((255, 255, 255, 190))
        self.screen.blit(veil, (0, 0))
        self._rounded((234, 286, 532, 170), COLORS["white"], 26, shadow=True)
        self._draw_icon("sparkle", (WIDTH // 2 - 135, 345), COLORS["success"], 25)
        self._text("¡Lo lograste!", self.title_font, COLORS["success"], (WIDTH // 2 + 5, 340),
                   center=True)
        self._text("¡Enhorabuena! Has completado el tablero.", self.font, COLORS["ink"],
                   (WIDTH // 2, 399), center=True, max_width=470)
        self._text("Pulsa «Nuevo» para seguir jugando", self.small_font, COLORS["muted"],
                   (WIDTH // 2, 430), center=True)

    def _draw_stat_card(
        self, label: str, value: str, rect: pygame.Rect, color: tuple[int, int, int],
    ) -> None:
        self._rounded(rect, color, 15)
        self._text(label, self.small_font, COLORS["muted"], (rect.centerx, rect.y + 8),
                   center=True, max_width=rect.width - 16)
        self._text(value, self.medium_font, COLORS["ink"], (rect.centerx, rect.y + 39),
                   center=True)

    def _draw_key_hint(self, key: str, label: str, position: tuple[int, int]) -> None:
        key_surface = self.small_font.render(key, True, COLORS["lavender_dark"])
        key_rect = key_surface.get_rect(topleft=position)
        key_rect.inflate_ip(12, 0)
        pygame.draw.rect(self.screen, COLORS["lavender"], key_rect, border_radius=6)
        self.screen.blit(key_surface, (key_rect.x + 6, key_rect.y))
        label_x = key_rect.right + 9
        self._text(label, self.small_font, COLORS["muted"], (label_x, position[1]),
                   max_width=920 - label_x)

    def _draw_button(
        self,
        name: str,
        label: str,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        icon: str,
    ) -> None:
        self.buttons[name] = rect
        self._rounded(rect, color, 14)
        self._draw_icon(icon, (rect.x + 25, rect.centery), COLORS["ink"], 16)
        label_x = rect.x + 46
        rendered_label = self.small_font.render(label, True, COLORS["ink"])
        label_rect = rendered_label.get_rect(midleft=(label_x, rect.centery))
        available_width = rect.right - 12 - label_x
        if label_rect.width > available_width:
            label_font = pygame.font.SysFont(
                self.font_family,
                max(12, self.small_font.get_height() - 1),
            )
            rendered_label = label_font.render(label, True, COLORS["ink"])
            label_rect = rendered_label.get_rect(midleft=(label_x, rect.centery))
        self.screen.blit(rendered_label, label_rect)

    def _draw_toast(self, message: str) -> None:
        rect = pygame.Rect(170, HEIGHT - 58, 660, 42)
        self._rounded(rect, COLORS["ink"], 14)
        self._text(message, self.small_font, COLORS["white"], rect.center, center=True)

    def _draw_decorations(self) -> None:
        pygame.draw.circle(self.screen, COLORS["lavender"], (947, 74), 34)
        self._draw_icon("sparkle", (947, 74), COLORS["lavender_dark"], 18)
        pygame.draw.circle(self.screen, COLORS["yellow"], (911, 97), 13)
        pygame.draw.circle(self.screen, COLORS["mint"], (39, 710), 22)
        pygame.draw.circle(self.screen, COLORS["blue"], (76, 731), 10)

    def _draw_icon(
        self, name: str, center: tuple[int, int], color: tuple[int, int, int], size: int,
    ) -> None:
        x, y = center
        half = size // 2
        width = max(2, size // 9)
        if name == "grid":
            for row in range(3):
                for col in range(3):
                    pygame.draw.rect(
                        self.screen, color,
                        (x - half + col * size // 3 + 1, y - half + row * size // 3 + 1,
                         size // 3 - 3, size // 3 - 3),
                        border_radius=2,
                    )
        elif name == "clock":
            pygame.draw.circle(self.screen, color, center, half, width)
            pygame.draw.line(self.screen, color, center, (x, y - half // 2), width)
            pygame.draw.line(self.screen, color, center, (x + half // 2, y + half // 3), width)
        elif name == "bulb":
            pygame.draw.circle(self.screen, color, (x, y - 2), half - 2, width)
            pygame.draw.line(self.screen, color, (x - half // 2, y + half // 3),
                             (x + half // 2, y + half // 3), width)
            pygame.draw.line(self.screen, color, (x - half // 3, y + half // 2),
                             (x + half // 3, y + half // 2), width)
        elif name == "pencil":
            points = [(x - half, y + half // 2), (x + half // 2, y - half),
                      (x + half, y - half // 2), (x - half // 2, y + half)]
            pygame.draw.polygon(self.screen, color, points)
            pygame.draw.line(self.screen, COLORS["white"], (x - half // 2, y + half // 4),
                             (x + half // 2, y - half // 2), width)
        elif name == "refresh":
            pygame.draw.arc(self.screen, color, (x - half, y - half, size, size),
                            0.5, 5.6, width)
            pygame.draw.polygon(self.screen, color, [(x + half, y - half // 2),
                             (x + half, y + half // 3), (x + half // 3, y - half // 6)])
        elif name == "home":
            pygame.draw.polygon(self.screen, color, [(x - half, y), (x, y - half),
                             (x + half, y), (x + half // 2, y), (x + half // 2, y + half),
                             (x - half // 2, y + half), (x - half // 2, y)])
        elif name == "easy":
            pygame.draw.ellipse(self.screen, color, (x - half, y - half // 2, size, size))
            pygame.draw.line(self.screen, COLORS["mint"], (x - half // 2, y + half // 3),
                             (x + half // 2, y - half // 3), width)
        elif name == "medium":
            for offset in (-half // 2, 0, half // 2):
                pygame.draw.circle(self.screen, color, (x + offset, y), max(2, width + 1))
        elif name == "hard":
            points = []
            for index in range(10):
                radius = half if index % 2 == 0 else half // 2
                angle = -1.5708 + index * 0.6283
                points.append((x + int(radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x),
                               y + int(radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y)))
            pygame.draw.polygon(self.screen, color, points)
        elif name == "pointer":
            pygame.draw.polygon(self.screen, color, [(x - half, y - half),
                             (x + half // 2, y + half // 3), (x, y + half // 2),
                             (x - half // 4, y + half), (x - half // 2, y - half // 3)])
        elif name in ("sparkle", "hint"):
            pygame.draw.line(self.screen, color, (x, y - half), (x, y + half), width)
            pygame.draw.line(self.screen, color, (x - half, y), (x + half, y), width)
            pygame.draw.line(self.screen, color, (x - half // 2, y - half // 2),
                             (x + half // 2, y + half // 2), width)
            pygame.draw.line(self.screen, color, (x + half // 2, y - half // 2),
                             (x - half // 2, y + half // 2), width)

    def _rounded(
        self, rect: pygame.Rect | tuple[int, int, int, int], color: tuple[int, int, int],
        radius: int, shadow: bool = False,
    ) -> None:
        rect = pygame.Rect(rect)
        if shadow:
            shadow_rect = rect.move(0, 5)
            pygame.draw.rect(self.screen, (231, 225, 224), shadow_rect, border_radius=radius)
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)

    def _text(
        self,
        value: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        position: tuple[int, int],
        center: bool = False,
        max_width: int | None = None,
    ) -> None:
        if max_width is not None:
            font_size = font.get_height()
            while font.size(value)[0] > max_width and font_size > 11:
                font_size -= 1
                font = pygame.font.SysFont(self.font_family, font_size, bold=font.get_bold())
        surface = font.render(value, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(surface, rect)


if __name__ == "__main__":
    SudokuGame().run()
