# quantum_shift/entities/objects.py
import pygame
import random
import math
from settings import *

class GameObject:
    """Base class for all interactive objects"""
    def __init__(self, x, y, width, height, object_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = object_type
        self.active = True
        self.interactable = True
        
    def update(self, dt):
        """Update object state"""
        pass
    
    def interact(self, player):
        """Handle interaction with player"""
        pass
    
    def can_interact_with(self, entity):
        """Check if entity can interact with this object"""
        if not self.interactable:
            return False
        return self.get_rect().colliderect(entity.get_rect())
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen):
        """Render object"""
        pass

class Rift(GameObject):
    """Space-time rift that needs to be repaired"""
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, "rift")
        self.repaired = False
        self.energy = 0
        self.max_energy = 100
        self.repair_rate = 50  # Energy per second when being repaired
        self.animation_time = 0
        self.particles = []
        
    def update(self, dt):
        """Update rift state"""
        self.animation_time += dt
        self.update_particles(dt)
        
        if self.repaired and len(self.particles) == 0:
            # Generate celebration particles
            for _ in range(5):
                self.particles.append({
                    'x': self.x + self.width/2 + (random.random() - 0.5) * 20,
                    'y': self.y + self.height/2 + (random.random() - 0.5) * 20,
                    'vel_x': (random.random() - 0.5) * 100,
                    'vel_y': (random.random() - 0.5) * 100,
                    'life': 2.0,
                    'max_life': 2.0
                })
    
    def interact(self, player):
        """Repair the rift"""
        if not self.repaired:
            self.energy += self.repair_rate * (1/60)  # Assuming 60 FPS
            if self.energy >= self.max_energy:
                self.repair()
    
    def repair(self):
        """Complete rift repair"""
        self.repaired = True
        self.interactable = False
    
    def update_particles(self, dt):
        """Update particle effects"""
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            particle['life'] -= dt
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def render(self, screen):
        """Render rift with effects"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if not self.repaired:
            # Render swirling rift
            for i in range(5):
                radius = 15 + i * 3
                angle = self.animation_time * 2 + i * 0.5
                offset_x = math.cos(angle) * (radius * 0.3)
                offset_y = math.sin(angle) * (radius * 0.3)
                
                alpha = max(0, 255 - i * 40)
                color = (255, 100, 255, alpha) if i % 2 == 0 else (100, 255, 255, alpha)
                
                # Create surface for transparency
                particle_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, color, (radius, radius), radius)
                screen.blit(particle_surf, (center_x + offset_x - radius, center_y + offset_y - radius))
            
            # Repair progress indicator
            if self.energy > 0:
                progress = self.energy / self.max_energy
                bar_width = self.width
                bar_height = 4
                bar_x = self.x
                bar_y = self.y - 10
                
                pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * progress, bar_height))
        
        else:
            # Render repaired rift (stable portal)
            pygame.draw.circle(screen, GREEN, (center_x, center_y), 20, 3)
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 15, 2)
        
        # Render particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            if alpha > 0:
                particle_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                particle_surf.fill((255, 255, 255, alpha))
                screen.blit(particle_surf, (particle['x'] - 3, particle['y'] - 3))

class PressurePlate(GameObject):
    """Pressure plate activated by player or clones"""
    def __init__(self, x, y):
        super().__init__(x, y, 48, 16, "pressure_plate")
        self.activated = False
        self.activation_count = 0
        self.required_count = 1
        
    def update(self, dt):
        """Update pressure plate state"""
        # Reset activation count each frame
        self.activation_count = 0
    
    def check_activation(self, entities):
        """Check if entities are activating the plate"""
        for entity in entities:
            if entity and self.get_rect().colliderect(entity.get_rect()):
                self.activation_count += 1
        
        self.activated = self.activation_count >= self.required_count
    
    def render(self, screen):
        """Render pressure plate"""
        color = GREEN if self.activated else RED
        
        # Base plate
        pygame.draw.rect(screen, color, self.get_rect())
        pygame.draw.rect(screen, WHITE, self.get_rect(), 2)
        
        # Activation indicators
        for i in range(self.required_count):
            indicator_x = self.x + 8 + i * 12
            indicator_y = self.y + 4
            indicator_color = GREEN if i < self.activation_count else (50, 50, 50)
            pygame.draw.circle(screen, indicator_color, (indicator_x, indicator_y), 4)

class MovingPlatform(GameObject):
    """Platform that moves between waypoints"""
    def __init__(self, x, y, waypoints, speed=50):
        super().__init__(x, y, 64, 16, "moving_platform")
        self.waypoints = waypoints
        self.speed = speed
        self.current_waypoint = 0
        self.direction = 1
        
    def update(self, dt):
        """Update platform movement"""
        if len(self.waypoints) < 2:
            return
        
        target = self.waypoints[self.current_waypoint]
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 5:  # Reached waypoint
            self.current_waypoint += self.direction
            if self.current_waypoint >= len(self.waypoints) or self.current_waypoint < 0:
                self.direction *= -1
                self.current_waypoint = max(0, min(self.current_waypoint, len(self.waypoints) - 1))
        else:
            # Move towards target
            move_x = (dx / distance) * self.speed * dt
            move_y = (dy / distance) * self.speed * dt
            self.x += move_x
            self.y += move_y
    
    def render(self, screen):
        """Render moving platform"""
        pygame.draw.rect(screen, PURPLE, self.get_rect())
        pygame.draw.rect(screen, WHITE, self.get_rect(), 2)
        
        # Direction indicator
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        if self.waypoints and len(self.waypoints) > self.current_waypoint:
            target = self.waypoints[self.current_waypoint]
            dx = target[0] - self.x
            dy = target[1] - self.y
            if dx != 0 or dy != 0:
                length = math.sqrt(dx*dx + dy*dy)
                arrow_x = center_x + (dx / length) * 20
                arrow_y = center_y + (dy / length) * 8
                pygame.draw.line(screen, YELLOW, (center_x, center_y), (arrow_x, arrow_y), 3)

class Portal(GameObject):
    """Portal that teleports entities"""
    def __init__(self, x, y, destination_x, destination_y):
        super().__init__(x, y, 32, 48, "portal")
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.cooldown = 0
        self.max_cooldown = 1.0
        self.animation_time = 0
        
    def update(self, dt):
        """Update portal state"""
        self.cooldown = max(0, self.cooldown - dt)
        self.animation_time += dt
    
    def interact(self, entity):
        """Teleport entity"""
        if self.cooldown <= 0:
            entity.x = self.destination_x
            entity.y = self.destination_y
            self.cooldown = self.max_cooldown
    
    def can_interact_with(self, entity):
        """Check if entity can use portal"""
        if self.cooldown > 0:
            return False
        return super().can_interact_with(entity)
    
    def render(self, screen):
        """Render portal with swirl effect"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Portal ring
        for i in range(3):
            radius = 12 + i * 4
            color_intensity = 255 - i * 60
            color = (0, color_intensity, 255) if self.cooldown <= 0 else (100, 100, 100)
            pygame.draw.circle(screen, color, (center_x, center_y), radius, 2)
        
        # Swirling effect
        if self.cooldown <= 0:
            for i in range(8):
                angle = self.animation_time * 3 + i * (math.pi / 4)
                spiral_x = center_x + math.cos(angle) * (8 + i)
                spiral_y = center_y + math.sin(angle) * (8 + i)
                pygame.draw.circle(screen, CYAN, (int(spiral_x), int(spiral_y)), 2)

class TimedPlatform(GameObject):
    """Platform that disappears after being stepped on"""
    def __init__(self, x, y, timer_duration=3.0):
        super().__init__(x, y, 48, 16, "timed_platform")
        self.timer_duration = timer_duration
        self.timer = timer_duration
        self.triggered = False
        self.visible = True
        
    def update(self, dt):
        """Update timed platform"""
        if self.triggered:
            self.timer -= dt
            if self.timer <= 0:
                self.visible = False
                self.interactable = False
    
    def trigger(self):
        """Start the countdown timer"""
        if not self.triggered:
            self.triggered = True
    
    def reset(self):
        """Reset platform state"""
        self.triggered = False
        self.timer = self.timer_duration
        self.visible = True
        self.interactable = True
    
    def render(self, screen):
        """Render timed platform"""
        if not self.visible:
            return
        
        # Platform color based on time remaining
        if not self.triggered:
            color = BLUE
        else:
            time_ratio = self.timer / self.timer_duration
            if time_ratio > 0.5:
                color = BLUE
            elif time_ratio > 0.25:
                color = ORANGE
            else:
                color = RED
        
        pygame.draw.rect(screen, color, self.get_rect())
        pygame.draw.rect(screen, WHITE, self.get_rect(), 2)
        
        # Timer indicator
        if self.triggered:
            bar_width = int(self.width * (self.timer / self.timer_duration))
            pygame.draw.rect(screen, GREEN, (self.x, self.y - 4, bar_width, 2))

# Factory function to create objects
def create_object(obj_type, x, y, **kwargs):
    """Factory function to create game objects"""
    if obj_type == "rift":
        return Rift(x, y)
    elif obj_type == "pressure_plate":
        return PressurePlate(x, y)
    elif obj_type == "moving_platform":
        waypoints = kwargs.get('waypoints', [(x, y), (x + 100, y)])
        speed = kwargs.get('speed', 50)
        return MovingPlatform(x, y, waypoints, speed)
    elif obj_type == "portal":
        dest_x = kwargs.get('dest_x', x + 100)
        dest_y = kwargs.get('dest_y', y)
        return Portal(x, y, dest_x, dest_y)
    elif obj_type == "timed_platform":
        duration = kwargs.get('duration', 3.0)
        return TimedPlatform(x, y, duration)
    else:
        return GameObject(x, y, 32, 32, obj_type)

# =============================================================================

