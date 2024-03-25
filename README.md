# UDP Client-Server Application

This is a simple UDP client-server application written in Python. It allows the client to send messages to the server, and the server echoes the messages back to the client.

## Requirements

- Python 3.x

## Usage

1. **Server Setup:**

   - Open a terminal and navigate to the directory containing `server.py`.
   - Run the server script using the following command:
     ```
     python server.py
     ```
   - The server will start and wait for incoming messages.

2. **Client Setup:**

   - Open another terminal and navigate to the directory containing `client.py`.
   - Run the client script using the following command:
     ```
     python client.py
     ```
   - The client will start, and you will be prompted to enter messages to send to the server.

3. **Sending Messages:**

   - Type your message in the client terminal and press Enter to send it to the server.
   - The server will echo the message back to the client, and you will see it in the client terminal.

4. **Exiting the Client:**

   - To quit the client, type 'q' or 'quit' and press Enter. This will terminate the client application gracefully.

5. **Exiting the Server:**

   - To quit the server, type 'q' or 'quit' and press Enter. This will terminate the server application gracefully.

## Note

- This application uses UDP (User Datagram Protocol) for communication, which is connectionless and does not guarantee message delivery or order.
- The server echoes back any message it receives from the client.
- Both the client and server use threads to send messages concurrently.
- The application is for demonstration purposes and does not include error handling or security features commonly found in production-grade applications.

# Tests (Work in Progress)

There is a `tests` folder in the application root directory containing two files: `test_client.py` and `test_server.py`. These files have placeholders for the tests, which are yet to be implemented. Unit tests for the client and server functionality are under development. Stay tuned for updates!
