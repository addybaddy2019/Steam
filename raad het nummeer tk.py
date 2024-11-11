import tkinter as tk
import random
from PIL import Image, ImageTk


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("600x400")


        self.background_image = Image.open(r"C:/Users/Anas/OneDrive/Desktop/Screenshot 2024-11-07 220925.png")
        self.background_image = self.background_image.resize((600, 400),
                                                             Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.welcome_label = tk.Label(root, text="Welcome to the Number Guessing Game!", fg="blue", bg="white")
        self.welcome_label.pack(pady=10)

        self.min_label = tk.Label(root, text="Enter the minimum number:", bg="white")
        self.min_label.pack()
        self.min_entry = tk.Entry(root)
        self.min_entry.pack()

        # Maximum number input
        self.max_label = tk.Label(root, text="Enter the maximum number:", bg="white")
        self.max_label.pack()
        self.max_entry = tk.Entry(root)
        self.max_entry.pack()

        # Attempts input
        self.attempts_label = tk.Label(root, text="Enter the number of attempts you'd like to have:", bg="white")
        self.attempts_label.pack()
        self.attempts_entry = tk.Entry(root)
        self.attempts_entry.pack()

        # Feedback label for guesses
        self.feedback_label = tk.Label(root, text="", bg="white")
        self.feedback_label.pack(pady=10)

        # Guess input
        self.guess_label = tk.Label(root, text="Enter your guess:", bg="white")
        self.guess_label.pack()
        self.guess_entry = tk.Entry(root)
        self.guess_entry.pack()

        # Guess button
        self.guess_button = tk.Button(root, text="Guess", command=self.check_guess)
        self.guess_button.pack(pady=5)

        # New Game button
        self.new_game_button = tk.Button(root, text="Start New Game", command=self.start_game)
        self.new_game_button.pack(pady=5)

        # Initialize game variables
        self.secret_number = None
        self.attempts_left = 0

    def start_game(self):
        try:
            min_number = int(self.min_entry.get())
            max_number = int(self.max_entry.get())
            self.attempts_left = int(self.attempts_entry.get())

            if min_number >= max_number or self.attempts_left <= 0:
                self.feedback_label.config(text="Invalid range or attempts. Please try again.", fg="red")
                return

            self.secret_number = random.randint(min_number, max_number)
            self.feedback_label.config(text="Game started! Make your first guess.", fg="green")
            self.guess_entry.delete(0, tk.END)

        except ValueError:
            self.feedback_label.config(text="Please enter valid numbers.", fg="red")

    def check_guess(self):
        if self.secret_number is None:
            self.feedback_label.config(text="Start a new game first!", fg="red")
            return

        try:
            guess = int(self.guess_entry.get())
            self.attempts_left -= 1

            if guess < self.secret_number:
                self.feedback_label.config(text="Too low! Try again.", fg="orange")
            elif guess > self.secret_number:
                self.feedback_label.config(text="Too high! Try again.", fg="orange")
            else:
                self.feedback_label.config(text=f"Congratulations! You guessed the number!", fg="green")
                self.secret_number = None  # End the game

            if self.attempts_left <= 0 and guess != self.secret_number:
                self.feedback_label.config(text=f"Game over! The correct number was {self.secret_number}.", fg="red")
                self.secret_number = None  # End the game

        except ValueError:
            self.feedback_label.config(text="Please enter a valid number.", fg="red")


# Run the game
root = tk.Tk()
game = NumberGuessingGame(root)
root.mainloop()
