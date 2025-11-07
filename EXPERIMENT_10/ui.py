import pygame


try:
    FONT = pygame.font.SysFont("Arial", 17)
    BIG_FONT = pygame.font.SysFont("Arial", 22, bold=True)
    SMALL_FONT = pygame.font.SysFont("Arial", 14)
except:
    FONT = pygame.font.SysFont("consolas", 18)
    BIG_FONT = pygame.font.SysFont("consolas", 22, bold=True)
    SMALL_FONT = pygame.font.SysFont("consolas", 15)

THEME = {
    "bg": (15, 15, 25),          
    "panel": (25, 25, 40),       
    "text": (220, 220, 255),     
    "text_dim": (150, 150, 180),   
    "text_header": (180, 180, 255),
    "button": (40, 40, 70),        
    "button_hover": (70, 70, 110),     
    "button_border": (100, 100, 255),
    "grid_bg": (5, 5, 15),  
    "grid": (30, 30, 45),        
    "wall": (10, 10, 20),        
    "start": (0, 255, 150),      
    "end": (255, 80, 100),       
    "visited": (60, 120, 220),    
    "frontier": (120, 90, 180),    
    "path": (0, 255, 180),        
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
        self.shadow_color = (20, 20, 20)
        self.shadow_offset = 3

    def draw(self, screen):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(screen, self.shadow_color, shadow_rect, border_radius=8)

        # Draw main button
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        # Draw border (thicker if hovered)
        border_width = 3 if self.hovered else 2
        pygame.draw.rect(screen, self.border_color, self.rect, border_width, border_radius=8)

        text_surf = FONT.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered


def draw_panel(screen, stats, total_width, total_height, grid_width):
    """Draws the right-side techy dashboard."""
    panel_x = grid_width
    panel_width = total_width - grid_width
    panel_rect = pygame.Rect(panel_x, 0, panel_width, total_height)
    pygame.draw.rect(screen, THEME["panel"], panel_rect)

    base_x = panel_x + 20
    panel_center_x = panel_x + panel_width // 2
    
    # Title
    title = BIG_FONT.render("MAZE SOLVER", True, THEME["text_header"])
    title_rect = title.get_rect(center=(panel_center_x, 40))
    screen.blit(title, title_rect)

    # Stats Section
    y = 100
    stats_title = FONT.render("STATS", True, THEME["text_header"])
    stats_title_rect = stats_title.get_rect(center=(panel_center_x, y))
    screen.blit(stats_title, stats_title_rect)
    
    y += 40
    for key, value in stats.items():
        label = FONT.render(f"{key}:", True, THEME["text_dim"])
        val = FONT.render(str(value), True, THEME["text"])
        screen.blit(label, (base_x, y))
        
        # --- FIX ---
        # Was: val_rect = val.get_rect(right=(panel_x + panel_width - 20, y))
        # This is incorrect. 'right' expects a number.
        # 'topright' expects a tuple (x, y).
        val_rect = val.get_rect(topright=(panel_x + panel_width - 20, y))
        # --- END FIX ---
        
        screen.blit(val, val_rect)
        y += 30

    # Separator
    y += 10
    pygame.draw.line(screen, THEME["grid"], (base_x, y), (total_width - 20, y), 2)
    y += 20

    # Controls Section
    controls_title = FONT.render("CONTROLS", True, THEME["text_header"])
    controls_title_rect = controls_title.get_rect(center=(panel_center_x, y))
    screen.blit(controls_title, controls_title_rect)
    y += 40

    # --- Updated, clearer controls text ---
    controls = [
        "Drag Start/End: Move",
        "L-Drag Empty: Draw Walls",
        "L-Drag Wall: Erase Walls",
        "R-Click: Set End",
        "Shift + R-Click: Set Start",
    ]
    
    for control in controls:
        text_surf = SMALL_FONT.render(control, True, THEME["text_dim"])
        screen.blit(text_surf, (base_x, y))
        y += 25