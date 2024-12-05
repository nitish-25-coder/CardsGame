import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox

# Define the properties of the cards("numbers","colors")
colors = ["Red", "Green", "Blue", "Yellow"]
numbers = list(range(1, 10))
deck = [f"{color} {number}" for color in colors for number in numbers]

# Shuffling the deck
random.shuffle(deck)

# Players
player1_hand = []
player2_hand = []

# give first three cards to each player
for _ in range(3):
    player1_hand.append(deck.pop())
    player2_hand.append(deck.pop())

# setup output window using tkinter
app = tk.Tk()
app.title("Card Game")
app.geometry("800x600")
app.configure(bg="green")

# Load the card images on the output window
card_images = {}
def load_card_images():
    for card in deck + player1_hand + player2_hand:
        color, number = card.split()
        img_path = f"images/{color.lower()}_{number}.png"  # Ensure these images exist
        img = Image.open(img_path).resize((80, 120))
        card_images[card] = ImageTk.PhotoImage(img)
load_card_images()

# Canvas to display cards
canvas = tk.Canvas(app, width=800, height=400, bg="green")
canvas.pack()

# Labels to show player hands
player1_label = tk.Label(app, text="Player 1", font=("Helvetica", 14), bg="green", fg="white")
player1_label.place(x=100, y=450)

player2_label = tk.Label(app, text="Player 2", font=("Helvetica", 14), bg="green", fg="white")
player2_label.place(x=600, y=450)

# Label to display winner
winner_label = tk.Label(app, text="", font=("Helvetica", 18, "bold"), bg="green", fg="yellow")
winner_label.place(x=300, y=50)

# Draw button functionality
def draw_card(player):
    global deck
    if not deck:
        messagebox.showinfo("Game Over", "No more cards in the deck!")
        return

    card = deck.pop()

    if player == 1:
        player1_hand.append(card)
        update_player_display(player1_hand, 1)
        throw_card(player1_hand, 1)
    elif player == 2:
        player2_hand.append(card)
        update_player_display(player2_hand, 2)
        throw_card(player2_hand, 2)

# Function to allow player to throw a card
def throw_card(hand, player):
    def on_card_click(event):
        x, y = event.x, event.y
        for i, card in enumerate(hand):
            x_start = 50 if player == 1 else 450
            card_x = x_start + i * 100
            if card_x <= x <= card_x + 80:
                thrown_card = hand.pop(i)
                update_player_display(hand, player)
                deck.insert(0, thrown_card)  # Put the thrown card back on top of the deck

                # Check for win condition after the card is thrown
                if check_win_conditions():
                    return  # Stop further interaction if a player has won
                return

    canvas.bind("<Button-1>", on_card_click)

# Update the display for player hands
def update_player_display(hand, player):
    x_start = 50 if player == 1 else 450
    y_start = 300
    canvas.delete(f"player{player}")
    for i, card in enumerate(hand):
        x = x_start + i * 100
        y = y_start
        canvas.create_image(x, y, image=card_images[card], anchor="nw", tags=f"player{player}")

# Initial display of player hands
update_player_display(player1_hand, 1)
update_player_display(player2_hand, 2)

# Check win conditions
def check_win_conditions():
    def has_winning_combination(hand):
        numbers = [card.split()[1] for card in hand]
        colors = [card.split()[0] for card in hand]
        number_count = any(numbers.count(num) >= 3 for num in numbers)
        color_count = any(colors.count(col) >= 3 for col in colors)
        return number_count or color_count

    if has_winning_combination(player1_hand):
        winner_label.config(text="Player 1 Wins!")
        disable_buttons()
        return True
    elif has_winning_combination(player2_hand):
        winner_label.config(text="Player 2 Wins!")
        disable_buttons()
        return True
    return False

# Disable buttons at the end of the game
def disable_buttons():
    player1_button.config(state="disabled")
    player2_button.config(state="disabled")

# Buttons for player actions
player1_button = tk.Button(app, text="Player 1 Draw", bg="blue", fg="white", font=("Helvetica", 14), command=lambda: draw_card(1))
player1_button.place(x=100, y=520, width=200, height=50)

player2_button = tk.Button(app, text="Player 2 Draw", bg="red", fg="white", font=("Helvetica", 14), command=lambda: draw_card(2))
player2_button.place(x=500, y=520, width=200, height=50)

app.mainloop()
