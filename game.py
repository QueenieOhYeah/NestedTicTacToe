import tkinter as tk
from tkinter import font
import random


class Player:
    id: int
    label: str
    color: str

    def __init__(self, id, label, color, player_type):
        self.id = id
        self.label = label
        self.color = color
        self.type = player_type


class TicTacToe:

    def __init__(self, n: int):
        self._size = n
        self._row = [0] * self._size
        self._col = [0] * self._size
        self._diag = 0
        self._anti_diag = 0
        self._is_end = False
        self._winner = None
        self._occupied = set()

    def move(self, row: int, col: int, player: Player) -> bool:
        if self.is_valid(row, col):
            if player.id == 1:
                self._row[row] += 1
                self._col[col] += 1
                if row == col:
                    self._diag += 1
                if row == self._size - 1 - col:
                    self._anti_diag += 1
            else:
                self._row[row] += -1
                self._col[col] += -1
                if row == col:
                    self._diag += -1
                if row == self._size - 1 - col:
                    self._anti_diag += -1
            self._occupied.add((row, col))
            if abs(self._row[row]) == self._size or abs(self._col[col]) == self._size or abs(
                    self._diag) == self._size or abs(self._anti_diag) == self._size and not self._is_end:
                self._is_end = True
                self._winner = player
            else:
                if len(self._occupied) == self._size ** 2:
                    self._is_end = True
            return True
        else:
            return False

    def is_end(self):
        return self._is_end

#    def is_winner(self):
#        return self._winner

    def is_valid(self, row: int, col: int):
        if (row, col) not in self._occupied:
            return True
        return False

#    def has_winner(self):
#        return self.is_end() and not self.is_tied()

    def is_tied(self):
        return self.is_end() and self._winner is None
        
    def reset(self):
        self._row = [0] * self._size
        self._col = [0] * self._size
        self._diag = 0
        self._anti_diag = 0
        self._is_end = False
        self._winner = None
        self._occupied = set()
        


HUMAN_MODE = 0
COMPUTER_MODE = 1
DEFAULT_PLAYERS = [
    Player(1, "X", "blue", HUMAN_MODE),
    Player(2, "O", "green", HUMAN_MODE),
]


class TicTacToeGame(TicTacToe):
    def __init__(self, n: int, sub_game_n: int, players=DEFAULT_PLAYERS):
        super().__init__(n)
        self._sub_game_size = sub_game_n
        self.games = []
        self.current_sub_game = None
        self._players = players
        self._player_index = 0
        self.current_player = self._players[self._player_index]
        for i in range(self._size):
            game_row = []
            for j in range(self._size):
                game_row.append(TicTacToe(self._sub_game_size))
            self.games.append(game_row)


    def move(self, row: int, col: int):
        game_row = row // self._size
        game_col = col // self._size
        move_row = row % self._size
        move_col = col % self._size
        game = self.games[game_row][game_col]
        move_success = game.move(move_row, move_col, self.current_player)

        if move_success:
            self.current_sub_game = game
            '''if sub-game is tied, do not update the meta-game'''
            if game.is_tied():
                pass
            elif game.is_end() and (game_row, game_col) not in self._occupied:
                self._occupied.add((game_row, game_col))
                if self.current_player.id == 1:
                    self._row[game_row] += 1
                    self._col[game_col] += 1
                    if game_row == game_col:
                        self._diag += 1
                    if game_row == self._size - 1 - game_col:
                        self._anti_diag += 1
                else:
                    self._row[game_row] += -1
                    self._col[game_col] += -1
                    if game_row == game_col:
                        self._diag += -1
                    if game_row == self._size - 1 - game_col:
                        self._anti_diag += -1
                if abs(self._row[game_row]) == self._size or abs(self._col[game_col]) == self._size or abs(
                        self._diag) == self._size or abs(self._anti_diag) == self._size:
                    self._is_end = True
                    self._winner = self.current_player
                else:
                    if len(self._occupied) == self._size ** 2:
                        self._is_end = True
        return move_success

    def toggle_player(self):
        '''toggle player'''
        self._player_index = not self._player_index
        self.current_player = self._players[self._player_index]

    def change_mode_to_computer(self):
        '''set to computer mode'''
        self._players[1].type = COMPUTER_MODE
        print("set to computer mode")
        print(self._players[1].type)

    def change_mode_to_human(self):
        '''set to human mode'''
        self._players[1].type = HUMAN_MODE
        print("set to human mode")
        print(self._players[1].type)

    def get_size(self):
        return self._size

    def get_sub_game_size(self):
        return self._sub_game_size


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._button_to_position = {} #mapping from button to row, col
        self._position_to_button = {} #mapping from row, col to button
        self._available = set() #set of available positions
        self._game = game
        self._create_board_display()
        self._create_player_mode()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Select player mode",
            font=font.Font(size=12, weight="bold"),
        )
        self.display.pack()

    def _create_player_mode(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        button1 = tk.Button(
            master=grid_frame,
            text="Human",
            font=font.Font(size=12, weight="bold"),
            activeforeground="Orange",
            activebackground="blue",
            fg="black",
            width=4,
            height=1,
        )
        button1.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="nsew"
        )
        button1.bind("<ButtonPress-1>", self.change_player_mode_to_human)

        button2 = tk.Button(
            master=grid_frame,
            text="Computer",
            font=font.Font(size=12, weight="bold"),
            activeforeground="Orange",
            activebackground="blue",
            fg="black",
            width=4,
            height=1,
        )
        button2.bind("<ButtonPress-1>", self.change_player_mode_to_computer)
        button2.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="nsew"
        )

    def change_player_mode_to_human(self, event):
        self._game.change_mode_to_human()
        self._update_display(msg="Set human mode", color="red")

    def change_player_mode_to_computer(self, event):
        self._game.change_mode_to_computer()
        self._update_display(msg="Set computer mode", color="red")

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.get_size() * self._game.get_sub_game_size()):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.get_size() * self._game.get_sub_game_size()):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="white",
                    width=2,
                    height=1,
                    highlightbackground="#3E4149",
                )
                button.bind("<ButtonPress-1>", self.play)
                self._button_to_position[button] = (row, col)
                self._position_to_button[(row,col)] = button
                self._available.add((row,col))
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
                
    def clear(self, row, col):
        '''Use to reset the tied sub-game. The function do:
        1. Update the buttons belonged to a sub-game
        2. Add the grids back to the available set'''
        start_row = row - row % self._game.get_sub_game_size()
        start_col = col - col % self._game.get_sub_game_size()
        for r in range(self._game.get_sub_game_size()):
            for c in range(self._game.get_sub_game_size()):
                self._available.add((start_row + r, start_col + c))
                button = self._position_to_button[(start_row + r, start_col + c)]
                button.config(text="")
    
                
    def play(self, event):
        '''Handle a player's move'''
        clicked_btn = event.widget
        row, col = self._button_to_position[clicked_btn]
        self._move(row, col, clicked_btn)
        if not self._game.is_end() and self._game.current_player.type == COMPUTER_MODE:
                '''random select one from available positions'''
                (row, col) = random.sample(self._available, 1)[0]
#                print(row,col)
                self._move(row, col, self._position_to_button[(row,col)])
            
    def _move(self, row, col, button):
        if self._game.move(row, col):
            self._update_button(button)
            self._available.remove((row,col))
            '''check if a sub-game is tied'''
            if self._game.current_sub_game.is_tied():
               self._game.current_sub_game.reset()
               self.clear(row,col)
            '''check the meta game status'''
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.is_end():
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
        
    
    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color


def main():
    METAGAME_SIZE = 3
    SUBGAME_SIZE = 3
    game = TicTacToeGame(METAGAME_SIZE , SUBGAME_SIZE)
    board = TicTacToeBoard(game)
    board.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
