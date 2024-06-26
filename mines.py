import random
import time
import threading
from termcolor import colored
class Minesweeper:
    def __init__(self, rows, cols, mines, coins):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.coins = coins
        self.board = [[0] * cols for _ in range(rows)]
        self.visited = [[False] * cols for _ in range(rows)]
        self.generate_mines()
        self.update_adjacent_mines()

    def generate_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] != -1:  # Not already a mine
                self.board[row][col] = -1  # Place mine
                mines_placed += 1

    def update_adjacent_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:  # If it's a mine, skip
                    continue
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= r + dr < self.rows and 0 <= c + dc < self.cols:
                            if self.board[r + dr][c + dc] == -1:
                                self.board[r][c] += 1

    def print_board(self, reveal=False):
        for r in range(self.rows):
            text = colored(chr(ord('1') + r), "blue", "on_cyan")
            print(text , end="")
            for c in range(self.cols):
                if not reveal and not self.visited[r][c]:
                    text = colored("? ","red","on_green")
                    print(text, end="")
                elif self.board[r][c] == -1:
                    text = colored("*"+" ","white","on_red", attrs=["reverse", "blink"])
                    print(text, end="")  # Mine
                else:
                    text = colored(str(self.board[r][c])+" ", "yellow","on_magenta")
                    print(text, end="")
            text = colored(" ","magenta","on_magenta")
            print(text)
        print(" ", end="")
        for i in range(self.cols):
            text = colored(chr(ord('a') + i)+" ", "blue", "on_cyan")
            print(text , end="")
        print()

    def reveal(self, row, col):
        if not self.visited[row][col]:
            self.visited[row][col] = True
            if self.board[row][col] == -1:  # Hit a mine
                return False
            elif self.board[row][col] == 0:  # Blank cell, reveal neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= row + dr < self.rows and 0 <= col + dc < self.cols:
                            self.reveal(row + dr, col + dc)
            return True
    def reveal_2x2(self, row, col):
        for dr in [0, 1]:
            for dc in [0, 1]:
                if 0 <= row + dr < self.rows and 0 <= col + dc < self.cols and self.board[row + dr][col + dc] != -1:
                    self.reveal(row + dr, col + dc)
    def reveal_3x3(self, row, col):
        if self.board[row][col] == -1:
            return  # Do not reveal if the selected cell is a mine
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < self.height and 0 <= c < self.width and not self.revealed[r][c]:
                    if self.board[r][c] != 0:
                        self.revealed[r][c] = True
                        print(f"Revealed cell at ({r}, {c}): {self.board[r][c]}")
                    
                        



def play_game():
    rows = 8
    cols = 8
    mines = 20
    coins = 0
    hearts = 1  # Start with one heart
    reveal_2x2 = 0
    reveal_3x3 = 0

    game = Minesweeper(rows, cols, mines, coins)
    game.print_board()

    start_time = time.time()

    def timer():
        time_limit = 5 * 60  # 5 minutes
        check_heart = False
        while True:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, time_limit - elapsed_time)
            if remaining_time == 0:
                print("Time's up! Game over.")
                game.print_board(reveal=True)
                break
            elif remaining_time <= 10:
                print("You have {} seconds left!".format(int(remaining_time)))
            elif remaining_time % 30 == 0:
                print("Time remaining: {:.0f} seconds".format(remaining_time))
            
            # Check if hearts should be checked for availability
            if not check_heart and elapsed_time >= 30:
                check_heart = True
            if check_heart and elapsed_time % 30 == 0:
                check_heart = False
                if hearts == 0:
                    print("You ran out of hearts! Game over.")
                    game.print_board(reveal=True)
                    break
                else:
                    hearts -= 1
                    print("You used a heart. You have {} hearts left.".format(hearts))
            time.sleep(1)

    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

    # Game loop
    first_move = True
    while True:
        method = None
        while method == None:
            print("I have:")
            print("\t" + str(reveal_3x3) + " 3x3 methods")
            print("\t" + str(reveal_2x2) + " 2x2 methods")
            print("\t" + str(coins) + " coins")
            print("\t" + str(hearts) + " hearts")
            method_in = input("What to do? (shopping = 4, reveal_3x3 = 3, reveal_2x2 = 2, classic = 1)").lower()
            if method_in == "3" and reveal_3x3 > 0:
                method = method_in
            elif method_in == "2" and reveal_2x2 > 0:
                method = method_in
            elif method_in == "1":
                method = method_in
            elif method_in == "4" and coins > 0:
                (coins, hearts, reveal_2x2, reveal_3x3) = shop(coins, hearts,reveal_2x2,reveal_3x3)
            else:
                print("I cannot do that.")

        row_input = input("Enter row to reveal (1-8): ")
        col_input = input("Enter column to reveal (a-h): ")
        # TODO: Verifz input

        if not row_input.isdigit() or not col_input.isalpha():
            print("Invalid input! Row should be a number between 1 and 8, column should be a letter between 'a' and 'h'.")
            continue

        row = int(row_input) - 1
        col = ord(col_input.lower()) - ord('a')

        if not (0 <= row < rows and 0 <= col < cols):
            print("Invalid input! Row should be between 1 and 8, column should be between 'a' and 'h'.")
            continue

        if first_move:
            if game.board[row][col] == -1:
                print("You can't hit a mine on the first move! Try again.")
                continue
            first_move = False

        clear = True
        if method == "1":
            clear = game.reveal(row, col)
        elif method == "2":
            reveal_2x2 -= 1   
            clear = game.reveal_2x2(row, col)
        elif method == "3":
            reveal_3x3 -= 1
            clear = game.reveal_3x3(row, col)
           
        if not clear:
            print("Game Over! You hit a mine.")
            game.print_board(reveal=True)
            break
        game.print_board()

        # Check if all non-mine cells are revealed
        if all(all(visited for visited in row) for row in game.visited):
            print("Congratulations! You've won!")
            game.print_board(reveal=True)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Time elapsed:", round(elapsed_time, 2), "seconds")

            # Calculate coins earned based on elapsed time
            if elapsed_time <= 150:  # 2 minutes and 30 seconds
                coins += 6
            elif elapsed_time <= 180:  # 3 minutes
                coins += 4
            elif elapsed_time <= 225:  # 3 minutes and 45 seconds
                coins += 2
            else:
                coins += 1
            break

           

    print("Coins earned:", coins)
    # Ask if the player wants to shop or play again
    choice = input("Do you want to go to the shop (shop) or play again (play)? ").lower()
    if choice == "shop":
        (coins, hearts, reveal_2x2, reveal_3x3) = shop(coins, hearts,reveal_2x2,reveal_3x3)
    elif choice == "play":
        play_game()

def shop(coins, hearts,reveal_2x2,reveal_3x3):
    print("Welcome to the shop!")
    print("You have {} coins, {} hearts, {} reveal_2x2 and {} reveal_3x3".format(coins, hearts, reveal_2x2, reveal_3x3))
    print("Here is shop items and what will cost each item.")
    print("Heart = 1 coin")
    print("reveal_2x2 = 2 coins")
    print("reveal_3x3 = 4 coins")
    print("random = 3 coins")
    
    while True:
        purchase = input("heart = 1, 2x2 = 2, 3x3 = 3, random = 4, exit = 5 ").lower()
        if purchase == "1" and coins >= 1:
            hearts += 1
            coins -= 1
            print("You bought a heart! You now have {} hearts and {} coins left.".format(hearts, coins))
        elif purchase == "2" and coins > 1:
            reveal_2x2 += 1
            coins -=2
            print("You bought a reveal_2x2! You now have {} reveal_2x2 and {} coins left.".format(reveal_2x2, coins))
        elif purchase == "3" and coins > 3:
            reveal_3x3 += 1
            coins -=4
            print("You bought a reveal_3x3! You now have {} reveal_3x3 and {} coins left.".format(reveal_3x3, coins))
        elif purchase == "4" and coins > 2:
            random_number = random.randint(1, 4)
            if random_number == 1:
                print ("nothing")
            elif random_number == 2:
                hearts += 1
                print ("you have won heart")
                print("You now have {} hearts and {} coins left.".format(hearts, coins))
            elif random_number == 3:
                reveal_2x2 += 1
                print("you have won reveal_2x2")
                print("You now have {} reveal_2x2 and {} coins left.".format(reveal_2x2, coins))
            else:
                reveal_3x3 += 1
                print("you have won reveal_3x3")
                print("You now have {} reveal_3x3 and {} coins left.".format(reveal_3x3, coins))
        elif purchase == "5":
            return coins, hearts, reveal_2x2, reveal_3x3
        else:
            print("We don´t have that.")

if __name__ == "__main__":
    play_game()



