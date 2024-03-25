"""UDP Client Module

This module implements a UDP client class for sending and receiving messages from a server.

Classes:
    Client: A class representing a UDP client for communication with a server.

Usage:
    To use this module, create an instance of the Client class and call its run method
    with the host address and port number of the server.

Example:
    client = Client()
    client.run("localhost", 12345)
"""

import socket
import threading
import sys
from typing import Tuple


class Client:
    """UDP client class for sending and receiving messages from a server.

    This class implements a UDP client that can send messages to a server
    and receive responses. It operates asynchronously, allowing for concurrent
    sending and receiving of messages.

    Attributes:
        running (bool): Flag indicating whether the client is running.
        client_socket (socket.socket): The client's socket for communication.
        receiver_thread (threading.Thread): The thread for receiving messages from the server.
        sender_thread (threading.Thread): The thread for sending messages to the server.

    Methods:
        receive_message: Receives messages from the server and prints them to the console.
        send_message: Allows the user to input messages and sends them to the server.
        run: Initializes the client, establishes connection with the server, and starts sender
            and receiver threads.
        stop: Stops the client and performs cleanup.

    """

    def __init__(self) -> None:
        self.running: bool = True
        self.client_socket: socket.socket = None
        self.receiver_thread: threading.Thread = None
        self.sender_thread: threading.Thread = None
        self.server_address: Tuple[str, int] = ()

    def receive_message(self) -> None:
        """Receive messages from the server.
        Listens for incoming messages from the
        server and prints them to the console.
        """
        while self.running:
            try:
                message, _ = self.client_socket.recvfrom(1024)
                print(f"Received message from server: {message.decode()}")
            except socket.error as socket_error:
                if socket.timeout:
                    pass
                else:
                    print(f"Socket error in receive_message: {socket_error}")
            except Exception as general_error:
                print(f"Failed to receive the message: {general_error}")

    def send_message(self) -> None:
        """Send messages to the server.

        Allows the user to input messages and sends them to the server.
        The method continues running until the user types 'quit' or 'q'.
        """
        try:
            while self.running:
                message = input("Type message to server ('quit' or 'q' to stop): \n")
                if message.lower() in ["quit", "q"]:
                    self.stop()
                    sys.exit(0)
                self.client_socket.sendto(message.encode(), self.server_address)
        except socket.error as socket_error:
            print(f"Socket error in send_message: {socket_error}")
        except Exception as general_error:
            print(f"Failed to send message: {general_error}")

    def run(self, host: str, port: int) -> None:
        """Run the client.

        Initializes the client, establishes a connection with the server
        located at the specified host and port, and starts the sender
        and receiver threads to manage message sending and receiving
        asynchronously.

        Args:
            host (str): The hostname or IP address of the server.
            port (int): The port number on which the server is listening.
        """
        try:
            self.server_address = (host, port)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_socket.settimeout(1)
            self.receiver_thread = threading.Thread(target=self.receive_message)
            self.sender_thread = threading.Thread(target=self.send_message)

            self.receiver_thread.start()
            self.sender_thread.start()

            self.receiver_thread.join()
            self.sender_thread.join()
        except socket.error as socket_error:
            print(f"Socket error in run_server: {socket_error}")
        except Exception as general_error:
            print(f"failed to run the client properly: {general_error}")
        finally:
            if self.client_socket:
                self.client_socket.close()

    def stop(self) -> None:
        """Stop the client.
        Sets the running flag to False to signal the receiver and sender threads
        to stop, joins the threads to wait for their completion, closes the client
        socket, and prints a message indicating that the client has stopped.
        """
        print("Stopping the client...")
        self.running = False
        try:
            if threading.current_thread() != self.receiver_thread:
                self.receiver_thread.join()
            if threading.current_thread() != self.sender_thread:
                self.sender_thread.join()
            if self.client_socket:
                self.client_socket.close()
        except socket.error as socket_error:
            print(f"failed to close the socket: {socket_error}")
        except Exception as general_exception:
            print(f"failed to stop the client gracefully: {general_exception}")
        print("Client stopped.")


if __name__ == "__main__":
    client = Client()
    try:
        client.run("localhost", 12345)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: client shutting down...")
        sys.exit(0)
