import panel as pn
import random



class connect4:

    # Update the self.board based on the game state
    def update_board(self):
        for row in range(self.board_height):
            for col in range(self.board_width):
                button = self.buttons[row * self.board_width + col]
                if self.board[row][col] == 1:
                    button.button_type = 'danger'
                elif self.board[row][col] == 2:
                    button.button_type = 'warning'
                else:
                    button.button_type = 'primary'
                button.disabled = self.board[row][col] != 0

    def play_connect4(self, event):
        if isinstance(event.obj, pn.widgets.Button) and self.game_stopped == 0:
            row = event.obj.row
            col = event.obj.col
            button = self.buttons[row * self.board_width + col]
            if self.is_valid_move(col):
                row = self.get_next_open_row(col)
                self.make_move(row, col, 1)
                self.update_board()
                if self.is_winner(1):
                    self.status_text.value = 'Player 1 wins!'
                    button.disabled = True
                    self.game_stopped = 1
                elif self.is_board_full():
                    self.status_text.value = 'It\'s a tie!'
                    button.disabled = True
                else:
                    # Computer's turn
                    col = self.get_computer_move()
                    row = self.get_next_open_row(col)
                    self.make_move(row, col, 2)
                    self.update_board()
                    if self.is_winner(2):
                        self.game_stopped = 2
                        self.status_text.value = 'Computer wins!'
                        button.disabled = True
                    elif self.is_board_full():
                        self.status_text.value = 'It\'s a tie!'
                        button.disabled = True
                    else:
                        self.update_board()

    def __init__(self):
        # Define the dimensions of the game self.board
        self.board_width = 7
        self.board_height = 6

        self.game_stopped = 0
        # Create the game self.board
        self.board = [[0] * self.board_width for _ in range(self.board_height)]

        self.board_widget = pn.GridBox(
            sizing_mode='fixed',
            width=350,
            height=300,
            ncols=self.board_width
        )

        self.buttons = []

        # Add the buttons to the self.board and assign the row and column attributes
        for row in range(self.board_height):
            for col in range(self.board_width):
                button = pn.widgets.Button(width=50, height=50)
                button.row = row
                button.col = col
                button.on_click(self.play_connect4)
                self.buttons.append(button)

        self.board_widget.extend(self.buttons)

        # Create the game self.board widget

        # Create the status text widget
        self.status_text = pn.widgets.StaticText(value='Player 1\'s turn')

        # Create the layout
        self.layout = pn.Column(self.board_widget, pn.Spacer(), pn.Spacer(), self.status_text)

        self.update_board()
        self.layout.show()

    def is_valid_move(self, col):
        if col < 0 or col >= self.board_width:
            return False
        return self.board[0][col] == 0


    def get_next_open_row(self, col):
        for row in range(self.board_height - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return -1


    def make_move(self, row, col, player):
        if (self.board[row][col] == 0) and self.game_stopped == 0:
            self.board[row][col] = player


    def is_winner(self, player):
        # Check horizontal locations
        for col in range(self.board_width - 3):
            for row in range(self.board_height):
                if (
                    self.board[row][col] == player
                    and self.board[row][col + 1] == player
                    and self.board[row][col + 2] == player
                    and self.board[row][col + 3] == player
                ):
                    return True

        # Check vertical locations
        for col in range(self.board_width):
            for row in range(self.board_height - 3):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col] == player
                    and self.board[row + 2][col] == player
                    and self.board[row + 3][col] == player
                ):
                    return True

        # Check positively sloped diagonals
        for col in range(self.board_width - 3):
            for row in range(self.board_height - 3):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col + 1] == player
                    and self.board[row + 2][col + 2] == player
                    and self.board[row + 3][col + 3] == player
                ):
                    return True

        # Check negatively sloped diagonals
        for col in range(self.board_width - 3):
            for row in range(3, self.board_height):
                if (
                    self.board[row][col] == player
                    and self.board[row - 1][col + 1] == player
                    and self.board[row - 2][col + 2] == player
                    and self.board[row - 3][col + 3] == player
                ):
                    return True

        return False


    def is_board_full(self):
        for col in range(self.board_width):
            if self.board[0][col] == 0:
                return False
        return True


    def get_computer_move(self):
        valid_moves = [col for col in range(self.board_width) if self.is_valid_move(col)]
        ret = random.choice(valid_moves)
        chosen = False
        for col in valid_moves:
            if (not chosen):
                row = self.get_next_open_row(col)
                # see if 1 would win with this cell
                if (row == -1):
                    continue
                self.board[row][col] = 2
                if (self.is_winner(2)):
                    ret = col
                    chosen = True
                self.board[row][col] = 0
                if (not chosen):
                    self.board[row][col] = 1
                    if (self.is_winner(1)):
                        ret = col
                    self.board[row][col] = 0
        return ret



def main():
# Update the self.board and display the layout
    x = connect4()

if __name__ == '__main__':
    main()

