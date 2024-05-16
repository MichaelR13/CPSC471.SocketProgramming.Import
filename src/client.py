import sys
from socket import *
import os



def run_client(server_name, server_port):
    # Create a socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_name, server_port))

    # Receive and print the initial welcome message
    welcome_message = client_socket.recv(1024).decode()
    print(welcome_message)

    # Allow the user to enter commands
    while True:
        print()
        user_input = input("ftp> ")

        # Send the user's command to the server
        client_socket.send(user_input.encode())

        # Break the loop and close the connection if the user types "quit"
        if user_input.lower() == "quit":
            print("Closing connection.")
            break

        # Receive and print the response from the server
        response = client_socket.recv(1024).decode()
        print(response)

        # If the response is a request to send a file, handle it
        if response == "send_file":
            print("'send_file' recieved from server.")
            file_name = user_input.split(" ")[1]
            send_file(client_socket, file_name)

    # Close the client socket
    client_socket.close()



def send_file(client_socket, file_name):
    file_path = os.path.join(os.path.dirname(__file__), "client_resources", file_name)

    try:
        # Get the total size of the file
        total_size = os.path.getsize(file_path)

        print(f"Sending file of size: {total_size} bytes")

        # Convert total_size to a 12-byte string
        size_header = str(total_size).ljust(12, ' ').encode('utf-8')

        # Send the header first
        client_socket.send(size_header)

        # Initialize the bytes_sent variable
        bytes_sent = 0

        with open(file_path, 'rb') as file:
            # Send the file in chunks
            data = file.read(1024)
            while data:
                client_socket.send(data)
                bytes_sent += len(data)  # Update the bytes_sent variable
                data = file.read(1024)

                # Print or use the bytes_sent value as needed
                print(f"Sent {bytes_sent} bytes out of {total_size} bytes")

            print(f"File '{file_name}' sent successfully.")
            success_message = client_socket.recv(1024).decode()
            print(success_message)
    
    except FileNotFoundError:
        print(f"File '{file_name}' not found in 'client_resources' folder.")
    except Exception as e:
        print(f"Error sending file '{file_name}': {e}")



if __name__ == "__main__":
    # Check if both server_name and server_port are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <serverName> <serverPort>")
        sys.exit(1)

    # Get server_name and server_port from command-line arguments
    server_name = sys.argv[1]

    try:
        # Convert the provided port argument to an integer
        server_port = int(sys.argv[2])
    except ValueError:
        print("Invalid port number. Please provide a valid integer.")
        sys.exit(1)

    run_client(server_name, server_port)
