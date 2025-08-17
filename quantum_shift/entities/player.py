# quantum_shift/entities/player.py
import pygame
from settings import *

class Player:
    def __init__(self, x, y, time_controller, gravity_system):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.energy = ENERGY_MAX
        
        # Systems
        self.time_controller = time_controller
        self.gravity_system = gravity_system
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Time trail effect
        self.trail_positions = []
        self.max_trail_length = 10
        
    def update(self, dt, keys):
        """Update player state"""
        if self.time_controller.is_rewinding():
            self.handle_rewind()
        else:
            self.handle_input(keys)
            self.apply_physics(dt)
            self.record_position()
        
        self.update_animation(dt)
        self.update_trail()
        self.regenerate_energy(dt)
    
    def handle_input(self, keys):
        """Handle player input"""
        # Horizontal movement
        self.vel_x = 0
        if keys[KEY_LEFT] or keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[KEY_RIGHT] or keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
        
        # Jumping
        if (keys[KEY_JUMP] or keys[pygame.K_UP]) and self.on_ground:
            gravity_mult = -1 if self.gravity_system.is_flipped() else 1
            self.vel_y = -JUMP_STRENGTH * gravity_mult
            self.on_ground = False
    
    def apply_physics(self, dt):
        """Apply physics to player"""
        # Apply gravity
        gravity_direction = 1 if not self.gravity_system.is_flipped() else -1
        self.vel_y += GRAVITY * gravity_direction * dt
        
        # Update position
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Simple ground collision (you'd expand this with proper collision system)
        ground_level = SCREEN_HEIGHT - 100 if not self.gravity_system.is_flipped() else 100
        
        if not self.gravity_system.is_flipped():
            if self.y + self.height >= ground_level:
                self.y = ground_level - self.height
                self.vel_y = 0
                self.on_ground = True
        else:
            if self.y <= ground_level:
                self.y = ground_level
                self.vel_y = 0
                self.on_ground = True
        
        # Screen boundaries
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
    
    def handle_rewind(self):
        """Handle time rewind"""
        rewind_data = self.time_controller.get_rewind_position()
        if rewind_data:
            self.x = rewind_data['x']
            self.y = rewind_data['y']
            self.vel_x = rewind_data['vel_x']
            self.vel_y = rewind_data['vel_y']
    
    def record_position(self):
        """Record position for time mechanics"""
        self.time_controller.record_frame({
            'x': self.x,
            'y': self.y,
            'vel_x': self.vel_x,
            'vel_y': self.vel_y,
            'facing_right': self.facing_right
        })
    
    def update_animation(self, dt):
        """Update animation"""
        self.animation_timer += dt
        if self.animation_timer >= 0.1:  # 10 FPS animation
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0
    
    def update_trail(self):
        """Update time trail effect"""
        self.trail_positions.append((self.x + self.width//2, self.y + self.height//2))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
    
    def regenerate_energy(self, dt):
        """Regenerate energy over time"""
        if self.energy < ENERGY_MAX:
            self.energy = min(ENERGY_MAX, self.energy + 20 * dt)
    
    def can_use_ability(self, cost):
        """Check if player can use ability"""
        return self.energy >= cost
    
    def use_energy(self, cost):
        """Use energy for abilities"""
        self.energy = max(0, self.energy - cost)
    
    def reset(self):
        """Reset player state"""
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.energy = ENERGY_MAX
        self.trail_positions.clear()
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen):
        """Render player"""
        # Render time trail
        for i, pos in enumerate(self.trail_positions):
            alpha = int(255 * (i / len(self.trail_positions)) * 0.5)
            if alpha > 0:
                trail_surf = pygame.Surface((4, 4))
                trail_surf.set_alpha(alpha)
                trail_surf.fill(CYAN)
                screen.blit(trail_surf, (pos[0] - 2, pos[1] - 2))
        
        # Render player body
        color = CYAN if not self.time_controller.is_rewinding() else YELLOW
        pygame.draw.rect(screen, color, self.get_rect())
        
        # Render facing direction
        if self.facing_right:
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width - 5, self.y + 10),
                (self.x + self.width + 5, self.y + self.height//2),
                (self.x + self.width - 5, self.y + self.height - 10)
            ])
        else:
            pygame.draw.polygon(screen, WHITE, [
                (self.x + 5, self.y + 10),
                (self.x - 5, self.y + self.height//2),
                (self.x + 5, self.y + self.height - 10)
            ])
        
        # Render gravity indicator
        if self.gravity_system.is_flipped():
            pygame.draw.circle(screen, RED, 
                             (int(self.x + self.width//2), int(self.y - 10)), 3)

# =============================================================================

