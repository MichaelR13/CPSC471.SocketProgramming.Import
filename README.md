# Socket-Connection-Project
Class Project for CPSC 471 to learn how to use a socket connection between devices and different networking protocols.

## **Group:**
- Justin Dong: donganhtuanjustin@csu.fullerton.edu
- Alexis Martin: alex_is_martin@csu.fullerton.edu
- Michael Rojas: michaels.rojas13@csu.fullerton.edu
- Jonathan Martin: sartholl@csu.fullerton.edu

## **Programming Language**
- **Python**

## **Getting Started**
**1. From within the /src folder start the server on desired port:**

```
python3 server.py <PORT>
```

**2. In a separtate terminal run the client on desired IP (127.0.0.1) and port:**

```
python3 client.py <IP> <PORT>
```

**3. Use desired commands:**

## **Terminal Commands**
```
get <FILENAME>
```
- This command is used to download a file from the server to the client.
```
put <FILENAME>
```
- This command is utilized to upload a file from the client to the server.
```
ls
```
- This command shows the list of files in the sever directory
```
help
```
- This command assists the user in understanding the functionality of each command, and how to execute each command.
```
quit
```
- This command terminates the connection between the client and server, allowing the user to exit the program.

## **Unique Features**
- Incorporation of a command handler a simpler user I/O
