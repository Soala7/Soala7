# quantum_shift/mechanics/time_controller.py
import pygame
from collections import deque
from settings import *

class TimeController:
    """Handles all time-based mechanics"""
    def __init__(self):
        self.frame_history = deque(maxlen=int(TIME_REWIND_DURATION * FPS))
        self.is_rewinding_time = False
        self.rewind_index = 0
        self.energy = ENERGY_MAX
        
    def update(self, dt):
        """Update time controller"""
        # Regenerate energy
        if self.energy < ENERGY_MAX and not self.is_rewinding_time:
            self.energy = min(ENERGY_MAX, self.energy + 30 * dt)
    
    def record_frame(self, frame_data):
        """Record a frame of movement data"""
        if not self.is_rewinding_time:
            self.frame_history.append(frame_data.copy())
    
    def start_rewind(self):
        """Start time rewind"""
        if self.energy >= ENERGY_REWIND_COST and len(self.frame_history) > 0:
            self.is_rewinding_time = True
            self.rewind_index = len(self.frame_history) - 1
            self.energy -= ENERGY_REWIND_COST
    
    def stop_rewind(self):
        """Stop time rewind"""
        self.is_rewinding_time = False
        self.rewind_index = 0
    
    def is_rewinding(self):
        """Check if currently rewinding"""
        return self.is_rewinding_time
    
    def get_rewind_position(self):
        """Get position data during rewind"""
        if self.is_rewinding_time and self.rewind_index >= 0:
            frame_data = self.frame_history[self.rewind_index]
            self.rewind_index = max(0, self.rewind_index - 2)  # Rewind speed
            return frame_data
        else:
            self.stop_rewind()
            return None
    
    def can_create_clone(self):
        """Check if can create a clone"""
        return (self.energy >= ENERGY_CLONE_COST and 
                len(self.frame_history) >= FPS)  # At least 1 second of history
    
    def get_movement_history(self):
        """Get movement history for clone creation"""
        if self.can_create_clone():
            self.energy -= ENERGY_CLONE_COST
            return list(self.frame_history)
        return []
    
    def reset(self):
        """Reset time controller"""
        self.frame_history.clear()
        self.is_rewinding_time = False
        self.rewind_index = 0
        self.energy = ENERGY_MAX
    
    def get_energy_percentage(self):
        """Get energy as percentage"""
        return int((self.energy / ENERGY_MAX) * 100)

# =============================================================================

