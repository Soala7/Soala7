# quantum_shift/ui/transitions.py
import pygame
import math
from settings import *

class Transitions:
    """Handles screen transitions and effects"""
    def __init__(self, game):
        self.game = game
        self.transition_active = False
        self.transition_type = None
        self.transition_progress = 0.0
        self.transition_duration = 1.0
        self.font = pygame.font.Font(None, 48)
        
    def start_level_transition(self):
        """Start level transition effect"""
        self.transition_active = True
        self.transition_type = "level_complete"
        self.transition_progress = 0.0
        self.transition_duration = 2.0
    
    def start_death_transition(self):
        """Start death transition effect"""
        self.transition_active = True
        self.transition_type = "death"
        self.transition_progress = 0.0
        self.transition_duration = 1.5
    
    def start_fade_transition(self):
        """Start fade transition effect"""
        self.transition_active = True
        self.transition_type = "fade"
        self.transition_progress = 0.0
        self.transition_duration = 1.0
    
    def update(self, dt):
        """Update transition effects"""
        if self.transition_active:
            self.transition_progress += dt / self.transition_duration
            
            if self.transition_progress >= 1.0:
                self.transition_active = False
                self.transition_progress = 0.0
    
    def render(self, screen):
        """Render transition effects"""
        if not self.transition_active:
            return
        
        if self.transition_type == "level_complete":
            self.render_level_complete(screen)
        elif self.transition_type == "death":
            self.render_death_effect(screen)
        elif self.transition_type == "fade":
            self.render_fade_effect(screen)
    
    def render_level_complete(self, screen):
        """Render level completion effect"""
        # Create celebration effect
        alpha = int(255 * (1.0 - abs(0.5 - self.transition_progress) * 2))
        
        # Background flash
        flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        flash_color = (0, 255, 0, min(alpha // 4, 50))
        flash_surf.fill(flash_color)
        screen.blit(flash_surf, (0, 0))
        
        # Success text
        if self.transition_progress > 0.2 and self.transition_progress < 0.8:
            text = self.font.render("RIFT STABILIZED", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(text, text_rect)
            
            level_text = pygame.font.Font(None, 24).render(f"Level {self.game.current_level - 1} Complete", True, WHITE)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(level_text, level_rect)
        
        # Particle effects
        for i in range(20):
            particle_progress = (self.transition_progress + i * 0.05) % 1.0
            if particle_progress < 0.8:
                x = SCREEN_WIDTH//2 + math.cos(i * 0.3 + self.transition_progress * 4) * 100 * particle_progress
                y = SCREEN_HEIGHT//2 + math.sin(i * 0.3 + self.transition_progress * 4) * 100 * particle_progress
                size = max(1, int(5 * (1.0 - particle_progress)))
                pygame.draw.circle(screen, GREEN, (int(x), int(y)), size)
    
    def render_death_effect(self, screen):
        """Render death effect"""
        # Red flash
        alpha = int(200 * (1.0 - self.transition_progress))
        death_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        death_surf.fill((255, 0, 0, alpha))
        screen.blit(death_surf, (0, 0))
        
        # Death text
        if self.transition_progress > 0.3 and self.transition_progress < 0.9:
            text = self.font.render("TIME FRACTURE", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
    
    def render_fade_effect(self, screen):
        """Render fade effect"""
        alpha = int(255 * self.transition_progress)
        fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fade_surf.fill((0, 0, 0, alpha))
        screen.blit(fade_surf, (0, 0))

# =============================================================================

