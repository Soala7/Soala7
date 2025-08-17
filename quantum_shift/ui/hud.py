# quantum_shift/ui/hud.py
import pygame
import math
from settings import *

class HUD:
    """Heads-up display for game information"""
    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # HUD elements positions
        self.energy_bar_rect = pygame.Rect(20, 20, 200, 20)
        self.lives_pos = (20, 50)
        self.level_pos = (20, 75)
        self.rifts_pos = (20, 100)
        
        # Ability cooldown indicators
        self.ability_icons = {
            'rewind': {'pos': (SCREEN_WIDTH - 200, 20), 'size': 30},
            'clone': {'pos': (SCREEN_WIDTH - 150, 20), 'size': 30},
            'gravity': {'pos': (SCREEN_WIDTH - 100, 20), 'size': 30}
        }
    
    def render(self, screen):
        """Render HUD elements"""
        self.render_energy_bar(screen)
        self.render_game_info(screen)
        self.render_ability_indicators(screen)
        self.render_minimap(screen)
    
    def render_energy_bar(self, screen):
        """Render energy bar"""
        # Background
        pygame.draw.rect(screen, (50, 50, 50), self.energy_bar_rect)
        pygame.draw.rect(screen, WHITE, self.energy_bar_rect, 2)
        
        # Energy fill
        if hasattr(self.game, 'time_controller'):
            energy_percent = self.game.time_controller.get_energy_percentage() / 100.0
            fill_width = int(self.energy_bar_rect.width * energy_percent)
            
            # Color based on energy level
            if energy_percent > 0.6:
                color = GREEN
            elif energy_percent > 0.3:
                color = YELLOW
            else:
                color = RED
            
            fill_rect = pygame.Rect(self.energy_bar_rect.x, self.energy_bar_rect.y, 
                                  fill_width, self.energy_bar_rect.height)
            pygame.draw.rect(screen, color, fill_rect)
        
        # Energy label
        energy_text = self.font_small.render("TIME ENERGY", True, WHITE)
        screen.blit(energy_text, (self.energy_bar_rect.x, self.energy_bar_rect.y - 15))
    
    def render_game_info(self, screen):
        """Render game information"""
        # Lives
        lives_text = self.font_medium.render(f"Lives: {self.game.lives}", True, WHITE)
        screen.blit(lives_text, self.lives_pos)
        
        # Level
        level_text = self.font_medium.render(f"Level: {self.game.current_level}", True, WHITE)
        screen.blit(level_text, self.level_pos)
        
        # Rifts fixed
        rifts_text = self.font_medium.render(f"Rifts Fixed: {self.game.rifts_fixed}", True, WHITE)
        screen.blit(rifts_text, self.rifts_pos)
    
    def render_ability_indicators(self, screen):
        """Render ability cooldown indicators"""
        # Rewind indicator
        rewind_icon = self.ability_icons['rewind']
        rewind_ready = True
        if hasattr(self.game, 'time_controller'):
            rewind_ready = self.game.time_controller.energy >= ENERGY_REWIND_COST
        
        color = CYAN if rewind_ready else (100, 100, 100)
        pygame.draw.rect(screen, color, 
                        (*rewind_icon['pos'], rewind_icon['size'], rewind_icon['size']), 2)
        
        # R key label
        r_text = self.font_small.render("R", True, WHITE)
        text_rect = r_text.get_rect(center=(rewind_icon['pos'][0] + rewind_icon['size']//2, 
                                           rewind_icon['pos'][1] + rewind_icon['size']//2))
        screen.blit(r_text, text_rect)
        
        # Clone indicator
        clone_icon = self.ability_icons['clone']
        clone_ready = True
        if hasattr(self.game, 'time_controller'):
            clone_ready = self.game.time_controller.can_create_clone()
        
        color = GREEN if clone_ready else (100, 100, 100)
        pygame.draw.rect(screen, color, 
                        (*clone_icon['pos'], clone_icon['size'], clone_icon['size']), 2)
        
        # C key label
        c_text = self.font_small.render("C", True, WHITE)
        text_rect = c_text.get_rect(center=(clone_icon['pos'][0] + clone_icon['size']//2, 
                                           clone_icon['pos'][1] + clone_icon['size']//2))
        screen.blit(c_text, text_rect)
        
        # Gravity indicator
        gravity_icon = self.ability_icons['gravity']
        gravity_flipped = False
        if hasattr(self.game, 'gravity_system'):
            gravity_flipped = self.game.gravity_system.is_flipped()
        
        color = PURPLE if gravity_flipped else WHITE
        pygame.draw.rect(screen, color, 
                        (*gravity_icon['pos'], gravity_icon['size'], gravity_icon['size']), 2)
        
        # G key label
        g_text = self.font_small.render("G", True, WHITE)
        text_rect = g_text.get_rect(center=(gravity_icon['pos'][0] + gravity_icon['size']//2, 
                                           gravity_icon['pos'][1] + gravity_icon['size']//2))
        screen.blit(g_text, text_rect)
    
    def render_minimap(self, screen):
        """Render minimap showing level layout"""
        minimap_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 120, 120, 90)
        pygame.draw.rect(screen, (20, 20, 40), minimap_rect)
        pygame.draw.rect(screen, WHITE, minimap_rect, 2)
        
        # Minimap label
        minimap_text = self.font_small.render("MINIMAP", True, WHITE)
        screen.blit(minimap_text, (minimap_rect.x, minimap_rect.y - 15))
        
        # Player position
        if self.game.player:
            player_x = minimap_rect.x + int((self.game.player.x / SCREEN_WIDTH) * minimap_rect.width)
            player_y = minimap_rect.y + int((self.game.player.y / SCREEN_HEIGHT) * minimap_rect.height)
            pygame.draw.circle(screen, CYAN, (player_x, player_y), 3)
        
        # Guards positions
        for guard in self.game.guards:
            guard_x = minimap_rect.x + int((guard.x / SCREEN_WIDTH) * minimap_rect.width)
            guard_y = minimap_rect.y + int((guard.y / SCREEN_HEIGHT) * minimap_rect.height)
            pygame.draw.circle(screen, RED, (guard_x, guard_y), 2)
        
        # Rifts positions
        for obj in self.game.objects:
            if obj.type == "rift":
                rift_x = minimap_rect.x + int((obj.x / SCREEN_WIDTH) * minimap_rect.width)
                rift_y = minimap_rect.y + int((obj.y / SCREEN_HEIGHT) * minimap_rect.height)
                color = GREEN if obj.repaired else PURPLE
                pygame.draw.circle(screen, color, (rift_x, rift_y), 2)

# =============================================================================

