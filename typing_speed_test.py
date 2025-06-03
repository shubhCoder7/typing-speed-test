import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Speed Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Fonts
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)

# Word list - common English words
word_list = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
    "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"
]

class TypingSpeedTest:
    def __init__(self):
        self.reset_game()
        self.game_state = "menu"  # menu, game, results

    def reset_game(self):
        self.current_word = ""
        self.user_input = ""
        self.words_typed = 0
        self.correct_words = 0
        self.start_time = 0
        self.time_left = 60  # 60 seconds game
        self.game_active = False
        self.accuracy = 0
        self.wpm = 0

    def get_random_word(self):
        return random.choice(word_list)

    def start_game(self):
        self.reset_game()
        self.current_word = self.get_random_word()
        self.start_time = time.time()
        self.game_active = True
        self.game_state = "game"

    def check_word(self):
        if self.user_input.strip() == self.current_word:
            self.correct_words += 1
        self.words_typed += 1
        self.user_input = ""
        self.current_word = self.get_random_word()

    def end_game(self):
        self.game_active = False
        self.game_state = "results"

        # Calculate WPM and accuracy
        if self.words_typed > 0:
            self.accuracy = (self.correct_words / self.words_typed) * 100
        else:
            self.accuracy = 0

        self.wpm = self.correct_words  # WPM is correct words in 1 minute

    def update(self):
        if self.game_active:
            elapsed_time = time.time() - self.start_time
            self.time_left = max(0, 60 - int(elapsed_time))

            if self.time_left <= 0:
                self.end_game()

    def draw_menu(self):
        screen.fill(WHITE)

        title = font_large.render("Typing Speed Test", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        instruction = font_medium.render("Press SPACE to start", True, BLUE)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 300))

        pygame.display.flip()

    def draw_game(self):
        screen.fill(WHITE)

        # Display time left
        time_text = font_medium.render(f"Time: {self.time_left}s", True, BLACK)
        screen.blit(time_text, (WIDTH - 150, 20))

        # Display words typed
        words_text = font_medium.render(f"Words: {self.words_typed}", True, BLACK)
        screen.blit(words_text, (50, 20))

        # Display current word
        word_text = font_large.render(self.current_word, True, BLUE)
        screen.blit(word_text, (WIDTH//2 - word_text.get_width()//2, 200))

        # Display user input
        input_color = GREEN if self.user_input == self.current_word else BLACK
        input_text = font_medium.render(self.user_input, True, input_color)
        screen.blit(input_text, (WIDTH//2 - input_text.get_width()//2, 300))

        # Input box
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 200, 290, 400, 60), 2)

        pygame.display.flip()

    def draw_results(self):
        screen.fill(WHITE)

        title = font_large.render("Results", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        wpm_text = font_medium.render(f"Words Per Minute: {self.wpm}", True, BLUE)
        screen.blit(wpm_text, (WIDTH//2 - wpm_text.get_width()//2, 200))

        accuracy_text = font_medium.render(f"Accuracy: {self.accuracy:.1f}%", True, BLUE)
        screen.blit(accuracy_text, (WIDTH//2 - accuracy_text.get_width()//2, 250))

        words_text = font_medium.render(f"Words Typed: {self.words_typed}", True, BLACK)
        screen.blit(words_text, (WIDTH//2 - words_text.get_width()//2, 300))

        correct_text = font_medium.render(f"Correct Words: {self.correct_words}", True, GREEN)
        screen.blit(correct_text, (WIDTH//2 - correct_text.get_width()//2, 350))

        restart_text = font_small.render("Press SPACE to restart or ESC to quit", True, BLACK)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 450))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.start_game()

                elif self.game_state == "game" and self.game_active:
                    if event.key == pygame.K_RETURN:
                        self.check_word()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        # Only add printable characters
                        if event.unicode.isprintable() and event.unicode != ' ':
                            self.user_input += event.unicode

                elif self.game_state == "results":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "menu"

        return True

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.handle_events()

            self.update()

            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "game":
                self.draw_game()
            elif self.game_state == "results":
                self.draw_results()

            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TypingSpeedTest()
    game.run()
