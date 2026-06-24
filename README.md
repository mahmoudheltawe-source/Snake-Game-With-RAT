# Snake RAT Project

## Project Members

- **Student 1:** Mahmoud Haj Yahya — 214445090
- **Student 2:** Kareem Haj Yahya — 213442973


**Course:** Network Security Topics  
**Lecturer:** Doron Ofek               
**Submission Date:** 24/6/2026

## Overview
This project demonstrates a basic client-server architecture through a Snake game.

Main files:
- `server.py` — creates the server, waits for a connection, sends messages, and displays returned results.
- `snake_game.py` — runs the Snake game and starts the client communication component in a background thread.

The project is written in Python. The graphical interface uses `tkinter`, and the communication uses TCP sockets.

## Project Structure
```text
RAT-Project/
├── server.py
├── snake_game.py
└── README.md
```

## Architecture
```text
+-------------------+        TCP socket        +-------------------+
|     server.py     | <----------------------> |   snake_game.py   |
| waits for client  |                          | Snake GUI         |
| sends messages    |                          | background client |
| shows responses   |                          | processes messages|
+-------------------+                          +-------------------+
```

## server.py
The server side is responsible for:
- Creating a TCP socket.
- Binding to an IP address and port.
- Listening for a client.
- Accepting the client connection.
- Sending messages.
- Receiving and displaying responses.
- Closing the connection.

Server flow:
```text
Create socket -> Bind -> Listen -> Accept -> Exchange messages -> Close
```

The server handles one client during each session.

## snake_game.py
This file contains:
1. The graphical Snake game.
2. The client communication component.

### Game Responsibilities
- Create the game window.
- Draw the snake and food.
- Move the snake according to keyboard input.
- Detect wall and body collisions.
- Increase the score after collecting food.
- Grow the snake.
- Display game over.
- Restart the game.

### Snake Representation
The snake is stored as a list of coordinates:
```python
self.snake = [
    (200, 200),
    (180, 200),
    (160, 200),
]
```

The first coordinate is the head. The rest represent the body.

### Game Loop
During each cycle:
1. Calculate the next head position.
2. Check collisions.
3. Add the new head.
4. Remove the tail if food was not collected.
5. Update score and length when food is collected.
6. Redraw the game.
7. Schedule the next cycle.

### Controls
```text
Up Arrow    -> Move up
Down Arrow  -> Move down
Left Arrow  -> Move left
Right Arrow -> Move right
```

The game prevents an immediate reverse direction.

## Tkinter
`Tkinter` is Python's standard library for graphical desktop interfaces.

It is used for:
- The main window.
- The game canvas.
- The score label.
- The restart button.
- Keyboard events.
- Snake and food graphics.

The graphical loop starts with:
```python
root.mainloop()
```

## Background Thread
The client communication runs in a separate thread:
```text
Main thread       -> Snake graphical interface
Background thread -> Server communication
```

This keeps the game responsive while the client waits for network messages.

## Communication Flow
```text
1. server.py starts and waits.
2. snake_game.py starts.
3. The Snake window opens.
4. The background client connects.
5. The server sends a message.
6. The client processes it.
7. The client returns a response.
8. The server displays the response.
```

## Connection Functions

The following functions implement the communication between `server.py` and `snake_game.py`.

### `xor_crypt()`

The `xor_crypt()` function is used by both the server and the client to transform messages before they are sent through the network.

It applies the XOR operation using the same shared key on both sides. Because XOR is reversible, applying the function again restores the original message.

```text
Original message -> xor_crypt() -> Transmitted data
Transmitted data -> xor_crypt() -> Original message
```

### `handle_client()`

The `handle_client()` function is implemented in `server.py`.

It manages the communication session with a connected client. The function receives input from the server side, transforms the message using `xor_crypt()`, sends it to the client, receives the returned response, restores the original response, and displays it in the server terminal.

The function continues handling messages until the connection is closed or the session ends.

### `start_server()`

The `start_server()` function is implemented in `server.py`.

It creates the TCP socket, binds it to the selected host and port, starts listening for incoming connections, and accepts a client connection.

After a client connects, the function passes the connected socket to `handle_client()` so that the communication session can begin.

```text
Create socket -> Bind -> Listen -> Accept -> handle_client()
```

### `connect_to_server()`

The `connect_to_server()` function is implemented in `snake_game.py`.

It creates the client socket and connects the Snake application to the IP address and port used by the server.

After the connection is established, it waits for messages from the server, restores them using `xor_crypt()`, processes the received request, and sends a response back to the server.

This function runs in a background thread so that the Snake graphical interface remains active and responsive while network communication is taking place.


## XOR Function
The project uses XOR to transform messages before transmission.

The same operation restores the original message:
```text
Original -> XOR -> Transmitted data -> XOR -> Original
```

Both sides must use the same XOR key.

## Requirements
- Python 3
- Tkinter
- Windows or Ubuntu
- `server.py`
- `snake_game.py`

Tkinter is normally included with Python on Windows.

Ubuntu installation:
```bash
sudo apt update
sudo apt install python3 python3-tk
```

## Running on One Computer
Use the same host and port in both files:
```python
HOST = "127.0.0.1"
PORT = 9999
```

Open two terminals in the project folder.

### Terminal 1 — Start the Server
Windows:
```powershell
python server.py
```

Ubuntu:
```bash
python3 server.py
```

### Terminal 2 — Start the Game
Windows:
```powershell
python snake_game.py
```
or just opening the game


Ubuntu:
```bash
python3 snake_game.py
```

The Snake window should open, and the client should connect in the background.

## Running on Two Computers
Both computers must be connected to the same local network.

In `snake_game.py`, replace localhost with the private IP address of the server computer:
```python
HOST = "192.168.1.10"
PORT = 9999
```

The server and client must use the same port.

## Stopping the Project
- Close the Snake window to stop the game.
- Press `Ctrl + C` in the server terminal to stop the server.

## Expected Result
```text
1. The server starts listening.
2. The Snake game starts.
3. The client connects.
4. The game remains responsive.
5. Both sides exchange messages.
6. The server displays returned results.
```

## Summary
The project combines a graphical Snake game with TCP client-server communication.

The game runs in the main thread, while the communication component runs in a background thread. This allows both parts to operate at the same time.
