import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox

# Define the properties of the cards ("numbers", "colors")
colors = ["Red", "Green", "Blue", "Yellow"]
numbers = list(range(1, 10))
deck = [f"{color} {number}" for color in colors for number in numbers]

# Shuffling the deck
random.shuffle(deck)

# Players' hands and discard pile
player1_hand = []
player2_hand = []
discard_pile = []

# Give first three cards to each player
for _ in range(3):
    player1_hand.append(deck.pop())
    player2_hand.append(deck.pop())

# Set up the output window using tkinter
app = tk.Tk()
app.title("Card Game")
app.geometry("1600x1000")  # Increased window size
app.configure(bg="green")

# Load the card images on the output window
card_images = {}


def load_card_images():
    for card in deck + player1_hand + player2_hand:
        color, number = card.split()
        img_path = f"images/{color.lower()}_{number}.png"  # Ensure these images exist
        img = Image.open(img_path).resize((100, 150))  # Increased size
        card_images[card] = ImageTk.PhotoImage(img)
    # Load special images for deck and discard
    deck_img = Image.open("images/deck.png").resize((100, 150))  # Increased size
    discard_img = Image.open("images/discard_placeholder.png").resize((100, 150))  # Increased size
    card_images["deck"] = ImageTk.PhotoImage(deck_img)
    card_images["discard_placeholder"] = ImageTk.PhotoImage(discard_img)


load_card_images()

# Canvas to display cards
canvas = tk.Canvas(app, width=1500, height=700, bg="green")  # Enlarged canvas height
canvas.pack()

# Labels for player hands
player1_label = tk.Label(app, text="Player 1", font=("Helvetica", 16, "bold"), bg="green", fg="white")
player1_label.place(x=200, y=800)

player2_label = tk.Label(app, text="Player 2", font=("Helvetica", 16, "bold"), bg="green", fg="white")
player2_label.place(x=1000, y=800)

# Label to display winner (hidden initially)
winner_label = tk.Label(app, text="", font=("Helvetica", 24, "bold"), bg="green", fg="yellow")
winner_label.place(x=700, y=300)

# Variable to track the current player (1 or 2)
current_player = 1


# Draw from deck or discard
def draw_from_deck(player):
    global current_player
    if not deck:
        messagebox.showinfo("Game Over", "No more cards in the deck!")
        return
    card = deck.pop()
    if player == 1:
        player1_hand.append(card)
        update_player_display(player1_hand, 1)
        current_player = 2  # Switch to the next player's turn
    elif player == 2:
        player2_hand.append(card)
        update_player_display(player2_hand, 2)
        current_player = 1  # Switch to the next player's turn
    check_win_conditions()


def draw_from_discard(player):
    global current_player
    if not discard_pile:
        messagebox.showinfo("Invalid Action", "No cards in the discard pile!")
        return
    card = discard_pile.pop()
    if player == 1:
        player1_hand.append(card)
        update_player_display(player1_hand, 1)
        current_player = 2  # Switch to the next player's turn
    elif player == 2:
        player2_hand.append(card)
        update_player_display(player2_hand, 2)
        current_player = 1  # Switch to the next player's turn
    check_win_conditions()


# Throw a card to the discard pile
def throw_card(hand, player, card_index):
    global current_player
    thrown_card = hand.pop(card_index)
    discard_pile.append(thrown_card)
    update_deck_and_discard_pile()
    update_player_display(hand, player)

    # Check for win condition after a card is thrown
    if check_win_conditions():
        display_winner(player)
        return  # Stop further interaction if a player has won

    if not hand:  # If the player has no more cards after throwing
        display_winner(player)


# Update the display for player hands
def update_player_display(hand, player):
    x_start = 200 if player == 1 else 1000
    y_start = 500  # Adjusted y position for alignment
    canvas.delete(f"player{player}")
    max_cards_per_row = 8  # Maximum cards in one row

    for i, card in enumerate(hand):
        x = x_start + (i % max_cards_per_row) * 120  # Adjusted horizontal spacing
        y = y_start + (i // max_cards_per_row) * 160  # Wrap to next row if needed
        card_id = canvas.create_image(x, y, image=card_images[card], anchor="nw", tags=f"player{player}")
        canvas.tag_bind(card_id, "<Button-1>", lambda e, i=i: throw_card(hand, player, i))


# Update the deck and discard pile
def update_deck_and_discard_pile():
    canvas.delete("deck", "discard")  # Clear existing deck and discard items

    # Place the deck image on the canvas
    deck_x, deck_y = 600, 250  # Adjusted position for better visibility
    canvas.create_image(deck_x, deck_y, image=card_images["deck"], anchor="nw", tags="deck")
    canvas.tag_bind("deck", "<Button-1>", lambda e: draw_from_deck(current_player))

    # Place the discard pile image next to the deck
    discard_x, discard_y = deck_x + 150, deck_y  # Right of the deck
    if discard_pile:
        top_card = discard_pile[-1]
        canvas.create_image(discard_x, discard_y, image=card_images[top_card], anchor="nw", tags="discard")
    else:
        canvas.create_image(discard_x, discard_y, image=card_images["discard_placeholder"], anchor="nw", tags="discard")
    canvas.tag_bind("discard", "<Button-1>", lambda e: draw_from_discard(current_player))


# Check win conditions
def check_win_conditions():
    def has_winning_combination(hand):
        numbers = [card.split()[1] for card in hand]
        colors = [card.split()[0] for card in hand]
        number_count = any(numbers.count(num) >= 3 for num in numbers)
        color_count = any(colors.count(col) >= 3 for col in colors)
        return number_count or color_count

    if has_winning_combination(player1_hand):
        return True
    elif has_winning_combination(player2_hand):
        return True
    return False


# Display the winner in the same window by clearing other elements
def display_winner(player):
    canvas.delete("all")  # Clear all items on the canvas
    winner_label.config(text=f"Player {player} Wins!")
    winner_label.place(x=700, y=300)  # Centered winner label


# Initial display of player hands and discard pile
update_player_display(player1_hand, 1)
update_player_display(player2_hand, 2)
update_deck_and_discard_pile()

app.mainloop()
