import random
import time
import json
import os

# Sample word categories
word_categories = {
    'easy': ['cat', 'dog', 'fish', 'bird', 'cow'],
    'medium': ['apple', 'orange', 'banana', 'grape', 'peach'],
    'hard': ['computer', 'science', 'programming', 'python', 'mathematics'],
    'themed': {
        'animals': ['lion', 'tiger', 'elephant', 'giraffe', 'zebra'],
        'countries': ['canada', 'brazil', 'france', 'germany', 'japan'],
        'movies': ['inception', 'avatar', 'titanic', 'gladiator', 'matrix'],
        'sports': ['cricket', 'football', 'tennis', 'hockey', 'rugby'],
        'space': ['galaxy', 'nebula', 'comet', 'asteroid', 'meteor'],
        'technology': ['internet', 'robotics', 'blockchain', 'quantum', 'ai']
    }
}

# Load or initialize leaderboard
def load_leaderboard():
    if os.path.exists('leaderboard.json'):
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    return {}

def save_leaderboard(leaderboard):
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f)

def choose_word(difficulty, theme=None):
    if theme:
        category = word_categories['themed'][theme]
    else:
        category = word_categories[difficulty]
    
    if not category:
        raise ValueError("Category is empty")
    
    return random.choice(category)

def display_word(word, guesses):
    return ' '.join([char if char in guesses else '_' for char in word])

def dynamic_scoreboard(players):
    print("\nCurrent Scores:")
    for player, score in players.items():
        print(f"{player}: {score}")

def main():
    print("Welcome to Hangman Game!🕹️")
    leaderboard = load_leaderboard()

    # Multiplayer setup
    num_players = 0
    while num_players not in range(2, 5):
        try:
            num_players = int(input("Enter the number of players (2-4): "))
        except ValueError:
            print("Invalid input. Please enter a number between 2 and 4.")

    players = {}
    for i in range(1, num_players + 1):
        name = input(f"Enter Player {i}'s name: ")
        players[name] = 0

    while True:
        for player in players:
            print(f"\n{player}'s turn! 🎮")
            difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
            while difficulty not in word_categories:
                difficulty = input("Invalid choice. Please choose easy, medium, or hard: ").lower()

            theme = input("Choose a theme (animals, countries, movies, sports, space, technology) or press Enter for no theme: ").lower()
            if theme and theme not in word_categories['themed']:
                print("Invalid theme. No theme will be applied.")
                theme = None

            # Set turns and hints based on difficulty
            if difficulty == 'easy':
                turns = 10
                max_hints = 1
                timeout = 7
            elif difficulty == 'medium':
                turns = 7
                max_hints = 2
                timeout = 10
            else:
                turns = 5
                max_hints = 3
                timeout = 15

            word = choose_word(difficulty, theme)
            guesses = ''
            hints_used = 0
            rounds = 0

            while rounds < 5:  # Limit rounds to prevent infinite loop
                rounds += 1
                print(f"\nRound {rounds}:")
                print("Guess the word:", display_word(word, guesses))
                print(f"You have {turns} turns left.")
                print(f"Hint usage: {hints_used}/{max_hints}")

                # Only show hint option if hints are available
                if hints_used < max_hints:
                    print("Options: Enter a letter to guess or type 'hint' for a hint.")
                else:
                    print("Options: Enter a letter to guess (no hints available). 🚫")

                # Challenge card example
                if random.random() < 0.3:  # 30% chance of a challenge card
                    print("🔥 Challenge! Guess the next letter in 5 seconds for bonus points!")

                start_time = time.time()
                action = input(f"Your input [⏱ {timeout}s]: ").lower()
                elapsed_time = time.time() - start_time

                if elapsed_time > timeout:
                    print("⏱ Time's up! Try again next time. 🕒")
                    break

                if action == 'hint' and hints_used < max_hints:
                    hint_letter = random.choice([char for char in word if char not in guesses])
                    guesses += hint_letter
                    hints_used += 1
                    turns -= 1
                    print(f"Hint: One of the letters is '{hint_letter}'. 🧠")
                    continue

                elif action == 'hint' and hints_used >= max_hints:
                    print("No more hints available! 🚫")
                    continue

                elif len(action) == 1 and action.isalpha():
                    if action in guesses:
                        print("You already guessed that letter. 🔁")
                    else:
                        guesses += action
                        if action not in word:
                            turns -= 1
                            print("Wrong guess! ❌")
                        else:
                            print("Good guess! ✅")
                else:
                    print("Invalid input. Please enter a single letter. ⚠️")

                if all(char in guesses for char in word):
                    print(f"🎉 Congratulations, {player}! You won! The word was: {word} 🎊")
                    players[player] += turns  # Add remaining turns to score
                    break

                if turns == 0:
                    print(f"❌ You lost! The word was: {word}. Better luck next time! 🥲")
                    break

            dynamic_scoreboard(players)

        play_again = input("Do you want to play another round? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye! 👋")
            break

    # Update leaderboard
    for player, score in players.items():
        if player in leaderboard:
            leaderboard[player] += score
        else:
            leaderboard[player] = score
    save_leaderboard(leaderboard)

    print("\nFinal Leaderboard:")
    for name, score in sorted(leaderboard.items(), key=lambda x: x[1], reverse=True):
        print(f"{name}: {score}")

if __name__ == "__main__":
    main()
