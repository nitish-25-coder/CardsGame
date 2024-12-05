# Card Game with Tkinter

## Description
This project is a graphical card game built using Python, Tkinter, and Pillow. It supports two players who draw and discard cards to achieve specific winning combinations. The game dynamically updates the interface to display player hands and the game state.

---

## Features

### Gameplay Mechanics
- A deck of cards is created using four colors (Red, Green, Blue, Yellow) and numbers (1–9).
- Cards are shuffled at the start of the game to ensure randomness.
- Each player starts with three cards.
- Players can draw a card from the deck and discard one card per turn.

### Winning Conditions
- A player wins if they collect:
  - Three cards of the same color.
  - Three cards of the same number.
- The game ends either when a player wins or the deck runs out of cards.

### Graphical User Interface (GUI)
- **Canvas**: Displays the cards in the players' hands.
- **Buttons**: Allow players to perform actions such as drawing cards.
- **Labels**: Show player names and the game’s status, including the winner.
- The interface uses a green background, resembling a card table.

### Card Images
- Each card is represented by an image stored in the `images/` folder.
- Images are dynamically loaded and resized for display.

### Error Handling
- Alerts players if the deck is empty.
- Disables interaction once a winner is declared.

---

## Installation

### Prerequisites
- Python 3.x
- Required libraries:
  - Tkinter (comes pre-installed with Python)
  - Pillow (PIL)

### Steps
1. Clone or download the repository.
2. Ensure the `images/` folder contains card images named as `{color}_{number}.png` (e.g., `red_1.png`).
3. Install the Pillow library if not already installed:
   ```bash
   pip install pillow
   ```
4. Run the program:
   ```bash
   python card_game.py
   ```

---

## How to Play
1. Launch the program by running the Python script.
2. Each player starts with three cards.
3. Players take turns:
   - Click the "Draw" button to draw a card.
   - Discard a card by clicking on it in your hand.
4. The game declares a winner if:
   - A player has three cards of the same color.
   - A player has three cards of the same number.
5. If the deck runs out of cards, the game ends with no winner.

---

## Folder Structure
```
project-directory/
|— card_game.py          # Main Python script
|— images/               # Folder containing card images
    |— red_1.png
    |— green_2.png
    |— ...
```


