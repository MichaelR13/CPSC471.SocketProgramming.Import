import os



class CommandHandler:
    def __init__(self, server_directory):
        self.server_directory = server_directory



    def handle_command(self, command, connection_socket):
        # Split the command into parts
        parts = command.split()

        # Check if the command is empty
        if not parts:
            return "Invalid command. Please enter a valid command."

        # Get the command keyword (convert to lowercase for case-insensitivity)
        cmd = parts[0].lower()

        # Check the command and call the appropriate handler
        if cmd == "get":
            return self.handle_get_command(parts)
        elif cmd == "put":
            return self.handle_put_command(parts, connection_socket)
        elif cmd == "ls":
            return self.handle_ls_command()
        elif cmd == "help":
            return self.handle_help_command()
        elif cmd == "quit":
            return "quit"  # Signal to quit the connection
        else:
            return "Invalid command. Please enter a valid command."



    def handle_get_command(self, parts):
        # Check if the 'get' command has the correct number of arguments
        if len(parts) != 2:
            return "Invalid 'get' command. Usage: get <file name>"

        # Extract the file name from the command
        file_name = parts[1]

        # Construct the full path to the file on the server
        file_path = os.path.join(self.server_directory, file_name)

        # Check if the file exists on the server
        if os.path.isfile(file_path):
            # If the file exists, open it in binary mode and read its content
            with open(file_path, "rb") as file:
                content = file.read()
                return content  # Return the file content to the client
        else:
            # If the file does not exist, return an error message
            return f"File '{file_name}' not found on the server."



    def handle_put_command(self, parts, connection_socket):
        # Check if the 'put' command has the correct number of arguments
        if len(parts) != 2:
            return "Invalid 'put' command. Usage: put <file name>"

        # Extract the file name from the command
        file_name = parts[1]

        # Construct the full path to the file on the server
        file_path = os.path.join(self.server_directory, file_name)

        # Check if the file already exists on the server
        if os.path.exists(file_path):
            return f"Error: File '{file_name}' already exists on the server."

        # Notify the client to send the file content
        print("Sending 'send_file' message to client.")
        connection_socket.send("send_file".encode())

        # Receive the 12-byte header containing the file size
        size_header = connection_socket.recv(12)
        if not size_header:
            return "Error receiving file size header"
        else:
            print("Client received 'send_file' and is now sending file.")

        # Convert the size_header to an integer
        total_size = int(size_header.decode('utf-8').rstrip())  # Remove trailing spaces

        # Print the size of the file to be received
        print(f"Client file size: {total_size} bytes")

        # Receive file content from the client
        file_content = b""
        bytes_received = 0
        while bytes_received < total_size:
            chunk = connection_socket.recv(min(1024, total_size - bytes_received))
            if not chunk:
                break
            file_content += chunk
            bytes_received += len(chunk)
            print(f"Received {bytes_received} bytes")

        # Write the received file content to the server file
        with open(file_path, "wb") as file:
            file.write(file_content)

        # Print a success message and return it to the client
        print(f"File '{file_name}' successfully uploaded to the server.")
        return f"File '{file_name}' successfully uploaded to the server."



    def handle_ls_command(self):
        # Get the list of files in the server directory
        file_list = os.listdir(self.server_directory)

        # Join the list of files into a string with newline separators
        file_list_str = "\n".join(file_list)

        # Return the formatted list of files to the client
        return file_list_str

    def handle_help_command(self):
        # Show a list of valid commands and their usage syntax
        help_str = """
        get <file name> - Download a file from the server to the client.
        put <file name> - Upload a file from the client to the server.
        ls              - List the files in the server's directory.
        help            - Show a list of valid commands.
        quit            - Quit the connection."""
        return help_str