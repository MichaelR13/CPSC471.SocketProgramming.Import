import os
import sys
from socket import *
from command_handler import CommandHandler



def handle_client(connection_socket, command_handler):
    # Send an initial welcome message to the client
    connection_socket.send("Welcome to the FTP server! Enter commands.".encode())

    # Keep handling commands until the client disconnects
    while True:
        # Receive the command from the client
        command = connection_socket.recv(1024).decode()

        # If the command is empty, the other side unexpectedly closed its socket
        if not command:
            print("Client disconnected unexpectedly.")
            exit(1)

        # Process the command using the CommandHandler
        response = command_handler.handle_command(command, connection_socket)

        if response == "quit":
            print("Received 'quit' command. Closing connection.")
            exit(0)

        # If the response is a file content, send it back to the client
        if isinstance(response, bytes):
            connection_socket.send(response)
        else:
            # Otherwise, send the regular response
            connection_socket.send(response.encode())

    # Close the client socket when the client disconnects
    connection_socket.close()



def start_server(port):
    # The IP address on which to listen
    server_name = "127.0.0.1"

    # Create a TCP socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Bind the socket to the specified port
    server_socket.bind((server_name, port))

    # Start listening for incoming connections
    server_socket.listen(1)

    print(f"The server is ready to receive on {server_name}:{port}")

    # Instantiate the CommandHandler with the server directory
    server_directory = os.path.join(os.path.dirname(__file__), "server_resources")
    command_handler = CommandHandler(server_directory)

    # Forever accept incoming connections
    while True:
        # Accept a connection; get client's socket
        connection_socket, addr = server_socket.accept()

        # Handle the client in a new thread or process
        handle_client(connection_socket, command_handler)



if __name__ == "__main__":
    # Check if a port number is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)

    try:
        # Convert the provided argument to an integer (the port number)
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Please provide a valid integer.")
        sys.exit(1)

    start_server(port)
