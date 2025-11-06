import pygame

# Fonts (main.py will handle pygame.init())
try:
    FONT = pygame.font.SysFont("Arial", 17)
    BIG_FONT = pygame.font.SysFont("Arial", 22, bold=True)
    SMALL_FONT = pygame.font.SysFont("Arial", 14)
except:
    FONT = pygame.font.SysFont("Consolas", 18)
    BIG_FONT = pygame.font.SysFont("Consolas", 22, bold=True)
    SMALL_FONT = pygame.font.SysFont("Consolas", 15)

# Modern aesthetic color theme
THEME = {
    "bg": (18, 18, 28),
    "panel": (35, 35, 55),
    "text": (240, 240, 255),
    "text_dim": (160, 160, 200),
    "text_header": (200, 200, 255),
    "button": (50, 50, 80),
    "button_hover": (90, 90, 140),
    "button_border": (120, 120, 255),
    "grid_bg": (12, 12, 22),
    "grid": (45, 45, 65),
    "wall": (18, 18, 28),
    "start": (0, 255, 150),
    "end": (255, 90, 100),
    "visited": (70, 130, 230),
    "frontier": (130, 100, 190),
    "path": (0, 255, 180),
    "shadow": (20, 20, 20)
}


class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = THEME["button"]
        self.hover_color = THEME["button_hover"]
        self.border_color = THEME["button_border"]
        self.text_color = THEME["text"]
        self.hovered = False
        self.shadow_offset = 4

    def draw(self, screen):
        # Draw subtle shadow for depth
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(screen, THEME["shadow"], shadow_rect, border_radius=8)

        # Draw button
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # Border
        border_width = 3 if self.hovered else 2
        pygame.draw.rect(screen, self.border_color, self.rect, border_width, border_radius=8)

        # Text
        text_surf = FONT.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered


def draw_panel(screen, stats, total_width, total_height, grid_width):
    """Draws a modern, techy right-side panel."""
    panel_x = grid_width
    panel_width = total_width - grid_width
    panel_rect = pygame.Rect(panel_x, 0, panel_width, total_height)
    pygame.draw.rect(screen, THEME["panel"], panel_rect, border_radius=12)

    base_x = panel_x + 25
    center_x = panel_x + panel_width // 2
    
    # Title
    title_surf = BIG_FONT.render("MAZE SOLVER", True, THEME["text_header"])
    title_rect = title_surf.get_rect(center=(center_x, 40))
    screen.blit(title_surf, title_rect)

    # Stats
    y = 100
    stats_title = FONT.render("STATS", True, THEME["text_header"])
    screen.blit(stats_title, stats_title.get_rect(center=(center_x, y)))
    y += 40

    for key, value in stats.items():
        label = FONT.render(f"{key}:", True, THEME["text_dim"])
        val = FONT.render(str(value), True, THEME["text"])
        screen.blit(label, (base_x, y))
        val_rect = val.get_rect(topright=(panel_x + panel_width - 25, y))
        screen.blit(val, val_rect)
        y += 30

    # Separator
    y += 10
    pygame.draw.line(screen, THEME["grid"], (base_x, y), (total_width - 25, y), 2)
    y += 20

    # Controls
    controls_title = FONT.render("CONTROLS", True, THEME["text_header"])
    screen.blit(controls_title, controls_title.get_rect(center=(center_x, y)))
    y += 35

    controls = [
        "Drag Start/End: Move",
        "L-Drag Empty: Draw Walls",
        "L-Drag Wall: Erase Walls",
        "R-Click: Set End",
        "Shift + R-Click: Set Start"
    ]
    for control in controls:
        control_surf = SMALL_FONT.render(control, True, THEME["text_dim"])
        screen.blit(control_surf, (base_x, y))
        y += 25

    # Footer shadow line for depth
    pygame.draw.line(screen, THEME["shadow"], (base_x, total_height - 50), (total_width - 25, total_height - 50), 2)
    