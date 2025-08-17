# quantum_shift/mechanics/collision.py
import pygame
from settings import *

class CollisionSystem:
    """Handles collision detection and response"""
    def __init__(self):
        self.tile_map = []
        self.solid_tiles = set()
        
    def check_collision(self, entity1, entity2):
        """Check collision between two entities"""
        return entity1.get_rect().colliderect(entity2.get_rect())
    
    def check_tile_collision(self, entity, tile_map):
        """Check collision with tile map"""
        entity_rect = entity.get_rect()
        collisions = []
        
        # Get tile coordinates
        left_tile = int(entity_rect.left // TILE_SIZE)
        right_tile = int((entity_rect.right - 1) // TILE_SIZE)
        top_tile = int(entity_rect.top // TILE_SIZE)
        bottom_tile = int((entity_rect.bottom - 1) // TILE_SIZE)
        
        # Check each tile
        for y in range(top_tile, bottom_tile + 1):
            for x in range(left_tile, right_tile + 1):
                if (0 <= y < len(tile_map) and 
                    0 <= x < len(tile_map[y]) and 
                    tile_map[y][x] in self.solid_tiles):
                    
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 
                                          TILE_SIZE, TILE_SIZE)
                    if entity_rect.colliderect(tile_rect):
                        collisions.append((x, y, tile_rect))
        
        return collisions
    
    def resolve_collision(self, entity, tile_rect, collision_side):
        """Resolve collision between entity and tile"""
        entity_rect = entity.get_rect()
        
        if collision_side == "top":
            entity.y = tile_rect.bottom
            if entity.vel_y < 0:
                entity.vel_y = 0
        elif collision_side == "bottom":
            entity.y = tile_rect.top - entity.height
            if entity.vel_y > 0:
                entity.vel_y = 0
                entity.on_ground = True
        elif collision_side == "left":
            entity.x = tile_rect.right
            if entity.vel_x < 0:
                entity.vel_x = 0
        elif collision_side == "right":
            entity.x = tile_rect.left - entity.width
            if entity.vel_x > 0:
                entity.vel_x = 0
    
    def get_collision_side(self, entity_rect, tile_rect):
        """Determine which side of the tile was hit"""
        # Calculate overlap on each axis
        x_overlap = min(entity_rect.right, tile_rect.right) - max(entity_rect.left, tile_rect.left)
        y_overlap = min(entity_rect.bottom, tile_rect.bottom) - max(entity_rect.top, tile_rect.top)
        
        if x_overlap < y_overlap:
            # Horizontal collision
            if entity_rect.centerx < tile_rect.centerx:
                return "right"
            else:
                return "left"
        else:
            # Vertical collision
            if entity_rect.centery < tile_rect.centery:
                return "bottom"
            else:
                return "top"

# =============================================================================

