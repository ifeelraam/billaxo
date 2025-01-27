import json
import emojis  # Ensure this is a module that provides emoji constants
from pyrogram.types import InlineKeyboardButton


class XOGame:
    def __init__(self, game_id: str, player1: dict, player2: dict = None) -> None:
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.winner_keys = []
        self.whose_turn = True  # True: Player1's turn, False: Player2's turn
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        # Creating initial board buttons (for the inline keyboard)
        self.board_keys = [
            [InlineKeyboardButton(
                ".",
                json.dumps({
                    "type": "K",
                    "coord": (i, j),
                    "end": False
                })
            ) for j in range(3)]
            for i in range(3)
        ]

    def is_draw(self) -> bool:
        """Check if the game is a draw"""
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    return False  # Found an empty spot, not a draw
        
        # Update board keys for the end of the game
        new_board_keys = []

        for i in range(3):
            temp = []
            for j in range(3):
                if self.board[i][j] == 0:
                    temp.append(InlineKeyboardButton(
                        ".",
                        json.dumps({"type": "K", "coord": (i, j), "end": True})
                    ))
                elif self.board[i][j] == 1:
                    temp.append(InlineKeyboardButton(
                        emojis.X_loser,
                        json.dumps({"type": "K", "coord": (i, j), "end": True})
                    ))
                else:
                    temp.append(InlineKeyboardButton(
                        emojis.O_loser,
                        json.dumps({"type": "K", "coord": (i, j), "end": True})
                    ))
            new_board_keys.append(temp)

        # Add Play Again button
        new_board_keys.append([InlineKeyboardButton(
            "Pʟᴀʏ ᴀɢᴀɪɴ!",
            json.dumps({"type": "R"})
        )])

        self.board_keys = new_board_keys
        return True

    def fill_board(self, player_id: int, coord: tuple) -> bool:
        """Fill the board if the chosen cell is empty and update button state"""
        if self.board[coord[0]][coord[1]]:  # If the cell is already filled, return False
            return False

        # Assign the move to the respective player
        if player_id == self.player1["id"]:
            self.board[coord[0]][coord[1]] = 1
            self.board_keys[coord[0]][coord[1]] = InlineKeyboardButton(
                emojis.X,
                json.dumps({"type": "K", "coord": coord, "end": False})
            )
        else:
            self.board[coord[0]][coord[1]] = 2
            self.board_keys[coord[0]][coord[1]] = InlineKeyboardButton(
                emojis.O,
                json.dumps({"type": "K", "coord": coord, "end": False})
            )

        return True

    def check_winner(self) -> bool:
        """Check if there is a winner and update the game board accordingly"""
        # Check rows, columns, and diagonals for a winner
        win_combinations = [
            [(0, 0), (0, 1), (0, 2)],  # Row 1
            [(1, 0), (1, 1), (1, 2)],  # Row 2
            [(2, 0), (2, 1), (2, 2)],  # Row 3
            [(0, 0), (1, 0), (2, 0)],  # Column 1
            [(0, 1), (1, 1), (2, 1)],  # Column 2
            [(0, 2), (1, 2), (2, 2)],  # Column 3
            [(0, 0), (1, 1), (2, 2)],  # Diagonal 1
            [(0, 2), (1, 1), (2, 0)]   # Diagonal 2
        ]
        
        # Check for a winner in any of the win combinations
        for combination in win_combinations:
            first_cell = self.board[combination[0][0]][combination[0][1]]
            if first_cell != 0 and all(self.board[x][y] == first_cell for x, y in combination):
                self.winner = self.player1 if first_cell == 1 else self.player2
                self.winner_keys = combination
                break

        if self.winner:
            # Update board to reflect the winner
            new_board_keys = []
            for i in range(3):
                temp = []
                for j in range(3):
                    cell_value = self.board[i][j]
                    if cell_value == 0:
                        temp.append(InlineKeyboardButton(
                            ".",
                            json.dumps({"type": "K", "coord": (i, j), "end": True})
                        ))
                    elif cell_value == 1:
                        # Highlight the winning X if it's part of the winner's combination
                        emoji = emojis.X if (i, j) in self.winner_keys else emojis.X_loser
                        temp.append(InlineKeyboardButton(
                            emoji,
                            json.dumps({"type": "K", "coord": (i, j), "end": True})
                        ))
                    else:
                        # Highlight the winning O if it's part of the winner's combination
                        emoji = emojis.O if (i, j) in self.winner_keys else emojis.O_loser
                        temp.append(InlineKeyboardButton(
                            emoji,
                            json.dumps({"type": "K", "coord": (i, j), "end": True})
                        ))
                new_board_keys.append(temp)

            # Add Play Again button after the game is over
            new_board_keys.append([InlineKeyboardButton(
                "Play again!",
                json.dumps({"type": "R"})
            )])

            self.board_keys = new_board_keys
            return True

        return False

    def reset_game(self):
        """Reset the game board to the initial state"""
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.board_keys = [
            [InlineKeyboardButton(
                ".",
                json.dumps({
                    "type": "K",
                    "coord": (i, j),
                    "end": False
                })
            ) for j in range(3)]
            for i in range(3)
        ]
        self.winner = None
        self.winner_keys = []
        self.whose_turn = True

    def __repr__(self):
        """Return a string representation of the current game board"""
        board_display = "\n"
        for row in self.board:
            for cell in row:
                if cell == 0:
                    board_display += ". "
                elif cell == 1:
                    board_display += emojis.X + " "
                else:
                    board_display += emojis.O + " "
            board_display += "\n"
        return board_display
