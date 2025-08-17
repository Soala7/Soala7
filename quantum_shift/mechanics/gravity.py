# quantum_shift/mechanics/gravity.py
import pygame
from settings import *

class GravitySystem:
    """Handles gravity manipulation mechanics"""
    def __init__(self):
        self.gravity_flipped = False
        self.flip_cooldown = 0
        self.max_cooldown = 0.5  # Half second cooldown
        
    def update(self, dt):
        """Update gravity system"""
        if self.flip_cooldown > 0:
            self.flip_cooldown -= dt
    
    def flip_gravity(self):
        """Flip gravity direction"""
        if self.flip_cooldown <= 0:
            self.gravity_flipped = not self.gravity_flipped
            self.flip_cooldown = self.max_cooldown
            return True
        return False
    
    def is_flipped(self):
        """Check if gravity is flipped"""
        return self.gravity_flipped
    
    def get_gravity_direction(self):
        """Get gravity direction multiplier"""
        return -1 if self.gravity_flipped else 1
    
    def reset(self):
        """Reset gravity to normal"""
        self.gravity_flipped = False
        self.flip_cooldown = 0

# =============================================================================

