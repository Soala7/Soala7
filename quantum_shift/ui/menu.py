# quantum_shift/ui/menu.py
import pygame
import random
from settings import *

class Menu:
    """Main menu system"""
    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.menu_items = [
            {"text": "Start Mission", "action": "start_game"},
            {"text": "Instructions", "action": "show_instructions"},
            {"text": "Quit", "action": "quit_game"}
        ]
        
        self.selected_item = 0
        self.show_instructions_screen = False
        
        # Background animation
        self.bg_particles = []
        for _ in range(50):
            self.bg_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vel_x': random.uniform(-20, 20),
                'vel_y': random.uniform(-20, 20),
                'size': random.randint(1, 3)
            })
    
    def handle_event(self, event):
        """Handle menu events"""
        if self.show_instructions_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.show_instructions_screen = False
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.execute_menu_action()
    
    def execute_menu_action(self):
        """Execute selected menu action"""
        action = self.menu_items[self.selected_item]["action"]
        
        if action == "start_game":
            self.game.start_game()
        elif action == "show_instructions":
            self.show_instructions_screen = True
        elif action == "quit_game":
            self.game.running = False
    
    def update(self):
        """Update menu animations"""
        for particle in self.bg_particles:
            particle['x'] += particle['vel_x'] * (1/60)
            particle['y'] += particle['vel_y'] * (1/60)
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
    
    def render(self, screen):
        """Render menu"""
        screen.fill(BACKGROUND_COLOR)
        
        if self.show_instructions_screen:
            self.render_instructions(screen)
        else:
            self.render_main_menu(screen)
    
    def render_main_menu(self, screen):
        """Render main menu"""
        # Render background particles
        for particle in self.bg_particles:
            color = (100, 100, 150, 128)
            pygame.draw.circle(screen, color[:3], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
        
        # Title
        title_text = self.font_large.render("TIME BREAKERS", True, CYAN)
        subtitle_text = self.font_medium.render("Quantum Shift", True, WHITE)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Menu items
        start_y = 300
        for i, item in enumerate(self.menu_items):
            color = CYAN if i == self.selected_item else WHITE
            text = self.font_medium.render(item["text"], True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, start_y + i * 50))
            
            # Highlight selected item
            if i == self.selected_item:
                highlight_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(screen, CYAN, highlight_rect, 2)
            
            screen.blit(text, text_rect)
        
        # Version info
        version_text = self.font_small.render("v1.0 - Use WASD/Arrows and Space", True, WHITE)
        version_rect = version_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        screen.blit(version_text, version_rect)
    
    def render_instructions(self, screen):
        """Render instructions screen"""
        screen.fill(BACKGROUND_COLOR)
        
        # Title
        title_text = self.font_large.render("INSTRUCTIONS", True, CYAN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(title_text, title_rect)
        
        # Instructions text
        instructions = [
            "OBJECTIVE:",
            "Fix space-time rifts using quantum abilities",
            "",
            "CONTROLS:",
            "WASD / Arrow Keys - Move",
            "SPACE - Jump",
            "R - Rewind Time (5 seconds)",
            "C - Create Clone",
            "G - Flip Gravity",
            "E - Interact with objects",
            "ESC - Pause/Menu",
            "",
            "MECHANICS:",
            "• Clones replay your last 5 seconds",
            "• Use clones to activate pressure plates",
            "• Avoid guards - they can see you!",
            "• Time abilities consume energy",
            "• Energy regenerates over time",
            "",
            "Press ESC or ENTER to return"
        ]
        
        y_offset = 120
        for line in instructions:
            if line.startswith("OBJECTIVE:") or line.startswith("CONTROLS:") or line.startswith("MECHANICS:"):
                color = CYAN
                font = self.font_medium
            elif line.startswith("•"):
                color = YELLOW
                font = self.font_small
            else:
                color = WHITE
                font = self.font_small
            
            if line:  # Skip empty lines
                text = font.render(line, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
                screen.blit(text, text_rect)
            
            y_offset += 25

# =============================================================================

