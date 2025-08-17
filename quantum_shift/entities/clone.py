# quantum_shift/entities/clone.py
import pygame
from settings import *

class Clone:
    def __init__(self, start_x, start_y, movement_history):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.width = 24
        self.height = 32
        
        self.movement_history = movement_history[:]  # Copy history
        self.current_frame = 0
        self.playback_timer = 0
        self.frame_duration = 1.0 / 60.0  # 60 FPS playback
        self.finished = False
        
        # Visual properties
        self.alpha = 180
        self.color = (0, 255, 255, self.alpha)  # Semi-transparent cyan
        
    def update(self, dt):
        """Update clone playback"""
        if self.finished or self.current_frame >= len(self.movement_history):
            self.finished = True
            return
        
        self.playback_timer += dt
        
        if self.playback_timer >= self.frame_duration:
            # Get current frame data
            frame_data = self.movement_history[self.current_frame]
            self.x = frame_data['x']
            self.y = frame_data['y']
            
            self.current_frame += 1
            self.playback_timer = 0
    
    def is_finished(self):
        """Check if clone has finished playback"""
        return self.finished
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen):
        """Render clone with transparency effect"""
        if self.finished:
            return
        
        # Create a surface with per-pixel alpha
        clone_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        clone_surf.fill((100, 200, 255, self.alpha))
        
        # Add clone identifier
        pygame.draw.rect(clone_surf, (150, 220, 255, self.alpha), 
                        (2, 2, self.width-4, self.height-4))
        
        # Render holographic effect
        for i in range(3):
            offset = i * 2
            glow_surf = pygame.Surface((self.width + offset*2, self.height + offset*2), 
                                     pygame.SRCALPHA)
            alpha = max(0, self.alpha - i * 60)
            glow_surf.fill((100, 200, 255, alpha))
            screen.blit(glow_surf, (self.x - offset, self.y - offset))
        
        screen.blit(clone_surf, (self.x, self.y))
        
        # Add clone number indicator
        font = pygame.font.Font(None, 24)
        text = font.render("C", True, WHITE)
        screen.blit(text, (self.x + self.width//2 - 6, self.y - 20))

# =============================================================================

# quantum_shift/entities/guard.py
import pygame
from settings import *
import math

class Guard:
    def __init__(self, x, y, patrol_points=None):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 32
        self.speed = 100
        
        # AI State
        self.state = "patrol"  # patrol, chase, search
        self.target = None
        self.patrol_points = patrol_points or [(x-100, y), (x+100, y)]
        self.current_patrol_index = 0
        self.patrol_direction = 1
        
        # Detection
        self.vision_range = 150
        self.vision_angle = 90  # degrees
        self.facing_angle = 0  # 0=right, 90=down, 180=left, 270=up
        self.alert_timer = 0
        self.max_alert_time = 3.0
        
        # Pathfinding
        self.path = []
        self.path_index = 0
        
        # Visual
        self.color = RED
        self.alert_level = 0  # 0=calm, 1=suspicious, 2=alert
        
    def update(self, dt, player, clones):
        """Update guard AI"""
        self.update_detection(player, clones)
        self.update_behavior(dt)
        self.update_movement(dt)
        self.update_visuals(dt)
    
    def update_detection(self, player, clones):
        """Update target detection"""
        all_targets = [player] + clones
        closest_target = None
        closest_distance = float('inf')
        
        for target in all_targets:
            if target and not getattr(target, 'finished', False):
                distance = math.sqrt((target.x - self.x)**2 + (target.y - self.y)**2)
                
                if distance <= self.vision_range and self.can_see_target(target):
                    if distance < closest_distance:
                        closest_target = target
                        closest_distance = distance
        
        if closest_target:
            self.target = closest_target
            self.state = "chase"
            self.alert_timer = self.max_alert_time
            self.alert_level = 2
        elif self.alert_timer > 0:
            self.state = "search"
            self.alert_level = 1
        else:
            self.state = "patrol"
            self.alert_level = 0
            self.target = None
    
    def can_see_target(self, target):
        """Check if target is within vision cone"""
        # Calculate angle to target
        dx = target.x - self.x
        dy = target.y - self.y
        angle_to_target = math.degrees(math.atan2(dy, dx))
        
        # Normalize angles
        angle_diff = abs(angle_to_target - self.facing_angle)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        return angle_diff <= self.vision_angle / 2
    
    def update_behavior(self, dt):
        """Update AI behavior based on state"""
        if self.state == "patrol":
            self.patrol_behavior()
        elif self.state == "chase":
            self.chase_behavior()
        elif self.state == "search":
            self.search_behavior(dt)
    
    def patrol_behavior(self):
        """Patrol between waypoints"""
        if not self.patrol_points:
            return
        
        target_point = self.patrol_points[self.current_patrol_index]
        dx = target_point[0] - self.x
        dy = target_point[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 10:  # Reached patrol point
            self.current_patrol_index += self.patrol_direction
            if self.current_patrol_index >= len(self.patrol_points):
                self.current_patrol_index = len(self.patrol_points) - 2
                self.patrol_direction = -1
            elif self.current_patrol_index < 0:
                self.current_patrol_index = 1
                self.patrol_direction = 1
        
        # Update facing direction
        if abs(dx) > abs(dy):
            self.facing_angle = 0 if dx > 0 else 180
        else:
            self.facing_angle = 90 if dy > 0 else 270
    
    def chase_behavior(self):
        """Chase the target"""
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            
            # Update facing direction
            if abs(dx) > abs(dy):
                self.facing_angle = 0 if dx > 0 else 180
            else:
                self.facing_angle = 90 if dy > 0 else 270
    
    def search_behavior(self, dt):
        """Search for lost target"""
        self.alert_timer -= dt
        
        # Rotate to search
        self.facing_angle = (self.facing_angle + 90 * dt) % 360
    
    def update_movement(self, dt):
        """Update guard position"""
        if self.state == "patrol":
            target_point = self.patrol_points[self.current_patrol_index]
            self.move_towards(target_point[0], target_point[1], dt)
        elif self.state == "chase" and self.target:
            chase_speed = self.speed * 1.5  # Guards move faster when chasing
            self.move_towards(self.target.x, self.target.y, dt, chase_speed)
    
    def move_towards(self, target_x, target_y, dt, speed=None):
        """Move towards target position"""
        if speed is None:
            speed = self.speed
        
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize and apply speed
            dx = (dx / distance) * speed * dt
            dy = (dy / distance) * speed * dt
            
            self.x += dx
            self.y += dy
    
    def update_visuals(self, dt):
        """Update visual effects"""
        # Update color based on alert level
        if self.alert_level == 0:
            self.color = RED
        elif self.alert_level == 1:
            self.color = ORANGE
        else:
            self.color = (255, 100, 100)  # Bright red when chasing
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen):
        """Render guard"""
        # Render vision cone when alert
        if self.alert_level > 0:
            self.render_vision_cone(screen)
        
        # Render guard body
        pygame.draw.rect(screen, self.color, self.get_rect())
        
        # Render facing direction
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Calculate direction vector
        angle_rad = math.radians(self.facing_angle)
        end_x = center_x + math.cos(angle_rad) * 20
        end_y = center_y + math.sin(angle_rad) * 20
        
        pygame.draw.line(screen, WHITE, (center_x, center_y), (end_x, end_y), 3)
        
        # Render alert indicator
        if self.alert_level > 0:
            alert_color = YELLOW if self.alert_level == 1 else RED
            pygame.draw.circle(screen, alert_color, 
                             (int(center_x), int(self.y - 10)), 5)
    
    def render_vision_cone(self, screen):
        """Render vision cone"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Calculate cone points
        angle_rad = math.radians(self.facing_angle)
        left_angle = angle_rad - math.radians(self.vision_angle / 2)
        right_angle = angle_rad + math.radians(self.vision_angle / 2)
        
        left_x = center_x + math.cos(left_angle) * self.vision_range
        left_y = center_y + math.sin(left_angle) * self.vision_range
        right_x = center_x + math.cos(right_angle) * self.vision_range
        right_y = center_y + math.sin(right_angle) * self.vision_range
        
        # Draw cone
        points = [(center_x, center_y), (left_x, left_y), (right_x, right_y)]
        
        # Create surface for transparency
        cone_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surf, (255, 255, 0, 30), points)
        screen.blit(cone_surf, (0, 0))

# =============================================================================

