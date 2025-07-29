import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 28)

class GuessTheNumberGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Guess the Number Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.game_mode = None  # 'human_guess' or 'ai_guess'
        self.min_range = 1
        self.max_range = 100
        self.target_number = None
        self.user_guess = ""
        self.attempts = 0
        self.max_attempts = 10
        self.game_over = False
        self.feedback = ""
        self.input_active = False
        
        # AI guessing variables
        self.ai_min = 1
        self.ai_max = 100
        self.ai_guess = None
        self.ai_attempts = 0
        
        # Input box
        self.input_box = pygame.Rect(300, 350, 200, 40)
        
    def draw_button(self, text, x, y, width, height, color, text_color=WHITE):
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)
        
        text_surface = font_medium.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        # Title
        title = font_large.render("Guess the Number Game", True, DARK_BLUE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = font_medium.render("Choose your game mode:", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Range display
        range_text = font_small.render(f"Range: {self.min_range} - {self.max_range}", True, GRAY)
        range_rect = range_text.get_rect(center=(WINDOW_WIDTH//2, 220))
        self.screen.blit(range_text, range_rect)
        
        # Buttons
        human_btn = self.draw_button("I'll Guess AI's Number", 200, 280, 400, 60, BLUE)
        ai_btn = self.draw_button("AI Will Guess My Number", 200, 360, 400, 60, GREEN)
        
        # Range adjustment buttons
        range_label = font_small.render("Adjust Range:", True, BLACK)
        self.screen.blit(range_label, (150, 460))
        
        min_down_btn = self.draw_button("-", 150, 490, 30, 30, GRAY)
        min_up_btn = self.draw_button("+", 190, 490, 30, 30, GRAY)
        max_down_btn = self.draw_button("-", 570, 490, 30, 30, GRAY)
        max_up_btn = self.draw_button("+", 610, 490, 30, 30, GRAY)
        
        min_text = font_small.render(f"Min: {self.min_range}", True, BLACK)
        max_text = font_small.render(f"Max: {self.max_range}", True, BLACK)
        self.screen.blit(min_text, (230, 500))
        self.screen.blit(max_text, (480, 500))
        
        return human_btn, ai_btn, min_down_btn, min_up_btn, max_down_btn, max_up_btn
    
    def draw_human_guess_game(self):
        self.screen.fill(WHITE)
        
        # Title
        title = font_large.render("Guess My Number!", True, DARK_BLUE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Range and attempts
        info_text = f"Range: {self.min_range} - {self.max_range} | Attempts: {self.attempts}/{self.max_attempts}"
        info_surface = font_medium.render(info_text, True, BLACK)
        info_rect = info_surface.get_rect(center=(WINDOW_WIDTH//2, 150))
        self.screen.blit(info_surface, info_rect)
        
        if not self.game_over:
            # Input prompt
            prompt = font_medium.render("Enter your guess:", True, BLACK)
            prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH//2, 280))
            self.screen.blit(prompt, prompt_rect)
            
            # Input box
            color = LIGHT_BLUE if self.input_active else WHITE
            pygame.draw.rect(self.screen, color, self.input_box)
            pygame.draw.rect(self.screen, BLACK, self.input_box, 2)
            
            # Input text
            text_surface = font_medium.render(self.user_guess, True, BLACK)
            self.screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 8))
            
            # Guess button
            guess_btn = self.draw_button("Guess!", 350, 420, 100, 40, GREEN)
        else:
            guess_btn = None
        
        # Feedback
        if self.feedback:
            color = GREEN if "Correct" in self.feedback or "won" in self.feedback else RED if "Too" in self.feedback else BLACK
            feedback_surface = font_medium.render(self.feedback, True, color)
            feedback_rect = feedback_surface.get_rect(center=(WINDOW_WIDTH//2, 480))
            self.screen.blit(feedback_surface, feedback_rect)
        
        # Back button
        back_btn = self.draw_button("Back to Menu", 50, 520, 150, 40, GRAY)
        
        return guess_btn, back_btn
    
    def draw_ai_guess_game(self):
        self.screen.fill(WHITE)
        
        # Title
        title = font_large.render("I'm Guessing Your Number!", True, DARK_BLUE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Instructions
        if self.ai_guess is None:
            instruction = f"Think of a number between {self.min_range} and {self.max_range}, then click Start!"
            start_btn = self.draw_button("Start Guessing", 300, 200, 200, 50, GREEN)
            too_high_btn = too_low_btn = correct_btn = None
        else:
            instruction = f"Attempts: {self.ai_attempts}"
            start_btn = None
            
            if not self.game_over:
                # AI's guess
                guess_text = font_large.render(f"My guess: {self.ai_guess}", True, BLUE)
                guess_rect = guess_text.get_rect(center=(WINDOW_WIDTH//2, 250))
                self.screen.blit(guess_text, guess_rect)
                
                # Response buttons
                too_high_btn = self.draw_button("Too High", 150, 350, 120, 50, RED)
                correct_btn = self.draw_button("Correct!", 340, 350, 120, 50, GREEN)
                too_low_btn = self.draw_button("Too Low", 530, 350, 120, 50, BLUE)
            else:
                too_high_btn = too_low_btn = correct_btn = None
        
        # Info text
        info_surface = font_medium.render(instruction, True, BLACK)
        info_rect = info_surface.get_rect(center=(WINDOW_WIDTH//2, 150))
        self.screen.blit(info_surface, info_rect)
        
        # Feedback
        if self.feedback:
            color = GREEN if "won" in self.feedback or "got it" in self.feedback else BLACK
            feedback_surface = font_medium.render(self.feedback, True, color)
            feedback_rect = feedback_surface.get_rect(center=(WINDOW_WIDTH//2, 450))
            self.screen.blit(feedback_surface, feedback_rect)
        
        # Back button
        back_btn = self.draw_button("Back to Menu", 50, 520, 150, 40, GRAY)
        
        return start_btn, too_high_btn, too_low_btn, correct_btn, back_btn
    
    def start_human_guess_game(self):
        self.target_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_over = False
        self.feedback = ""
        self.user_guess = ""
    
    def start_ai_guess_game(self):
        self.ai_min = self.min_range
        self.ai_max = self.max_range
        self.ai_guess = None
        self.ai_attempts = 0
        self.game_over = False
        self.feedback = ""
    
    def make_human_guess(self):
        try:
            guess = int(self.user_guess)
            if guess < self.min_range or guess > self.max_range:
                self.feedback = f"Please enter a number between {self.min_range} and {self.max_range}"
                return
            
            self.attempts += 1
            
            if guess == self.target_number:
                self.feedback = f"Correct! You won in {self.attempts} attempts!"
                self.game_over = True
            elif guess < self.target_number:
                self.feedback = "Too low! Try a higher number."
            else:
                self.feedback = "Too high! Try a lower number."
            
            if self.attempts >= self.max_attempts and not self.game_over:
                self.feedback = f"Game over! The number was {self.target_number}"
                self.game_over = True
                
            self.user_guess = ""
            
        except ValueError:
            self.feedback = "Please enter a valid number"
    
    def make_ai_guess(self):
        if self.ai_guess is None:
            self.ai_guess = (self.ai_min + self.ai_max) // 2
            self.ai_attempts = 1
        
    def ai_response(self, response):
        self.ai_attempts += 1
        
        if response == "correct":
            self.feedback = f"I got it! The number was {self.ai_guess} in {self.ai_attempts} attempts!"
            self.game_over = True
        elif response == "too_high":
            self.ai_max = self.ai_guess - 1
            if self.ai_min <= self.ai_max:
                self.ai_guess = (self.ai_min + self.ai_max) // 2
            else:
                self.feedback = "Something went wrong! Are you sure about your responses?"
                self.game_over = True
        elif response == "too_low":
            self.ai_min = self.ai_guess + 1
            if self.ai_min <= self.ai_max:
                self.ai_guess = (self.ai_min + self.ai_max) // 2
            else:
                self.feedback = "Something went wrong! Are you sure about your responses?"
                self.game_over = True
    
    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            human_btn, ai_btn, min_down_btn, min_up_btn, max_down_btn, max_up_btn = self.draw_menu()
            
            if human_btn.collidepoint(mouse_pos):
                self.game_mode = 'human_guess'
                self.start_human_guess_game()
            elif ai_btn.collidepoint(mouse_pos):
                self.game_mode = 'ai_guess'
                self.start_ai_guess_game()
            elif min_down_btn.collidepoint(mouse_pos) and self.min_range > 1:
                self.min_range -= 1
            elif min_up_btn.collidepoint(mouse_pos) and self.min_range < self.max_range - 1:
                self.min_range += 1
            elif max_down_btn.collidepoint(mouse_pos) and self.max_range > self.min_range + 1:
                self.max_range -= 1
            elif max_up_btn.collidepoint(mouse_pos) and self.max_range < 1000:
                self.max_range += 1
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.game_mode is None:
                    self.handle_menu_events(event)
                
                elif self.game_mode == 'human_guess':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        guess_btn, back_btn = self.draw_human_guess_game()
                        
                        if self.input_box.collidepoint(mouse_pos):
                            self.input_active = True
                        else:
                            self.input_active = False
                        
                        if back_btn.collidepoint(mouse_pos):
                            self.game_mode = None
                        elif guess_btn and guess_btn.collidepoint(mouse_pos) and self.user_guess:
                            self.make_human_guess()
                    
                    elif event.type == pygame.KEYDOWN and self.input_active:
                        if event.key == pygame.K_RETURN and self.user_guess:
                            self.make_human_guess()
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_guess = self.user_guess[:-1]
                        elif event.unicode.isdigit() and len(self.user_guess) < 10:
                            self.user_guess += event.unicode
                
                elif self.game_mode == 'ai_guess':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        start_btn, too_high_btn, too_low_btn, correct_btn, back_btn = self.draw_ai_guess_game()
                        
                        if back_btn.collidepoint(mouse_pos):
                            self.game_mode = None
                        elif start_btn and start_btn.collidepoint(mouse_pos):
                            self.make_ai_guess()
                        elif too_high_btn and too_high_btn.collidepoint(mouse_pos):
                            self.ai_response("too_high")
                        elif too_low_btn and too_low_btn.collidepoint(mouse_pos):
                            self.ai_response("too_low")
                        elif correct_btn and correct_btn.collidepoint(mouse_pos):
                            self.ai_response("correct")
            
            # Draw current screen
            if self.game_mode is None:
                self.draw_menu()
            elif self.game_mode == 'human_guess':
                self.draw_human_guess_game()
            elif self.game_mode == 'ai_guess':
                self.draw_ai_guess_game()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GuessTheNumberGame()
    game.run()