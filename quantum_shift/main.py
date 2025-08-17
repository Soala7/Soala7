# quantum_shift/main.py
import pygame
import sys
import random
import math
from settings import *
from ui.menu import Menu
from ui.hud import HUD
from ui.transitions import Transitions
from entities.player import Player
from entities.guard import Guard
from mechanics.time_controller import TimeController
from mechanics.gravity import GravitySystem
from mechanics.collision import CollisionSystem
from utils.level_loader import LevelLoader

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Time Breakers: Quantum Shift")
        self.clock = pygame.time.Clock()
        
        # Game systems
        self.menu = Menu(self)
        self.hud = HUD(self)
        self.transitions = Transitions(self)
        self.time_controller = TimeController()
        self.gravity_system = GravitySystem()
        self.collision_system = CollisionSystem()
        self.level_loader = LevelLoader()
        
        # Game state
        self.state = "menu"
        self.current_level = 1
        self.lives = 3
        self.rifts_fixed = 0
        self.running = True
        
        # Entities
        self.player = None
        self.clones = []
        self.guards = []
        self.objects = []
        self.level_data = None
        
    def load_level(self, level_num):
        """Load a specific level"""
        self.level_data = self.level_loader.load_level(level_num)
        if self.level_data:
            self.player = Player(
                self.level_data['player_start'][0],
                self.level_data['player_start'][1],
                self.time_controller,
                self.gravity_system
            )
            self.guards = [Guard(pos[0], pos[1]) for pos in self.level_data['guards']]
            self.objects = self.level_data['object_instances']
            self.clones = []
            return True
        return False
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "menu":
                self.menu.handle_event(event)
            elif self.state == "playing":
                self.handle_game_events(event)
    
    def handle_game_events(self, event):
        """Handle gameplay events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "menu"
            elif event.key == pygame.K_r:
                self.time_controller.start_rewind()
            elif event.key == pygame.K_c:
                self.create_clone()
            elif event.key == pygame.K_g:
                self.gravity_system.flip_gravity()
            elif event.key == pygame.K_e:
                self.interact_with_objects()
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self.time_controller.stop_rewind()
    
    def create_clone(self):
        """Create a clone from recorded movement"""
        if self.time_controller.can_create_clone():
            from entities.clone import Clone
            clone = Clone(
                self.player.x, self.player.y,
                self.time_controller.get_movement_history()
            )
            self.clones.append(clone)
    
    def interact_with_objects(self):
        """Handle object interactions"""
        for obj in self.objects:
            if obj.can_interact_with(self.player):
                obj.interact(self.player)
    
    def update(self):
        """Update all game systems"""
        if self.state == "playing":
            self.update_game()
        elif self.state == "menu":
            self.menu.update()
    
    def update_game(self):
        """Update gameplay systems"""
        dt = self.clock.get_time() / 1000.0
        
        # Update time controller
        self.time_controller.update(dt)
        
        # Update entities
        if self.player:
            self.player.update(dt, pygame.key.get_pressed())
            
        for clone in self.clones[:]:
            clone.update(dt)
            if clone.is_finished():
                self.clones.remove(clone)
        
        for guard in self.guards:
            guard.update(dt, self.player, self.clones)
        
        for obj in self.objects:
            obj.update(dt)
        
        # Check collisions
        self.check_collisions()
        
        # Check win conditions
        self.check_level_complete()
    
    def check_collisions(self):
        """Handle all collision detection"""
        if not self.player:
            return
            
        # Player-Guard collisions
        for guard in self.guards:
            if self.collision_system.check_collision(self.player, guard):
                self.handle_player_caught()
        
        # Player-Object collisions
        for obj in self.objects:
            if obj.type == "rift" and self.collision_system.check_collision(self.player, obj):
                self.repair_rift(obj)
    
    def handle_player_caught(self):
        """Handle when player is caught by guard"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over()
        else:
            self.respawn_player()
    
    def repair_rift(self, rift):
        """Repair a space-time rift"""
        if not rift.repaired:
            rift.repair()
            self.rifts_fixed += 1
    
    def check_level_complete(self):
        """Check if level objectives are complete"""
        if self.level_data:
            rifts_in_level = sum(1 for obj in self.objects if obj.type == "rift")
            repaired_rifts = sum(1 for obj in self.objects if obj.type == "rift" and obj.repaired)
            
            if repaired_rifts >= rifts_in_level:
                self.complete_level()
    
    def complete_level(self):
        """Handle level completion"""
        self.current_level += 1
        if self.load_level(self.current_level):
            self.transitions.start_level_transition()
        else:
            self.state = "victory"
    
    def respawn_player(self):
        """Respawn player at start position"""
        if self.level_data and self.player:
            self.player.x, self.player.y = self.level_data['player_start']
            self.player.reset()
            self.clones.clear()
            self.time_controller.reset()
    
    def game_over(self):
        """Handle game over"""
        self.state = "game_over"
    
    def start_game(self):
        """Start the game"""
        self.current_level = 1
        self.lives = 3
        self.rifts_fixed = 0
        if self.load_level(self.current_level):
            self.state = "playing"
        else:
            print("Failed to load level 1")
    
    def render(self):
        """Render everything"""
        self.screen.fill(BACKGROUND_COLOR)
        
        if self.state == "menu":
            self.menu.render(self.screen)
        elif self.state == "playing":
            self.render_game()
        elif self.state == "game_over":
            self.render_game_over()
        elif self.state == "victory":
            self.render_victory()
        
        pygame.display.flip()
    
    def render_game(self):
        """Render gameplay"""
        # Render level background
        if self.level_data:
            self.level_loader.render_level(self.screen, self.level_data)
        
        # Render objects
        for obj in self.objects:
            obj.render(self.screen)
        
        # Render entities
        for guard in self.guards:
            guard.render(self.screen)
            
        for clone in self.clones:
            clone.render(self.screen)
        
        if self.player:
            self.player.render(self.screen)
        
        # Render UI
        self.hud.render(self.screen)
        
        # Render transitions
        self.transitions.render(self.screen)
    
    def render_game_over(self):
        """Render game over screen"""
        font = pygame.font.Font(None, 74)
        text = font.render("MISSION FAILED", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press ESC to return to menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
    
    def render_victory(self):
        """Render victory screen"""
        font = pygame.font.Font(None, 74)
        text = font.render("MISSION COMPLETE", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

# =============================================================================

