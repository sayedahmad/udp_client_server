"""UDP server module for handling communication with clients.

This module provides functionality for creating and managing a UDP server
that can receive messages from clients, send responses, and allow interaction
with connected clients. The server operates in a non-blocking manner,
allowing it to handle multiple clients concurrently.

Classes:
    UDPServer: Represents a UDP server capable of handling communication with clients.

Usage:
    To use this module, instantiate the UDPServer class and call its run_server
    method, providing the desired host and port. The server will start listening
    for incoming connections and handle client interactions.

Example:
    from server import UDPServer

    # Create a UDP server instance
    server = UDPServer()

    # Run the server on localhost and port 12345
    server.run_server("localhost", 12345)
"""

import socket
import threading
import sys
import time


class UDPServer:
    """UDP server class for receiving and responding to messages from clients.
    This class provides functionality for creating and managing a UDP server
    that can receive messages from clients, send responses, and allow interaction
    with connected clients. The server operates in a non-blocking manner,
    allowing it to handle multiple clients concurrently.

    Attributes:
        last_client_address (tuple): The address of the last connected client.
        lock (threading.Lock): A lock for thread synchronization.
        server_socket (socket.socket): The server's socket for communication.
        receiver_thread (threading.Thread): The thread for receiving messages.
        user_thread (threading.Thread): The thread for sending user messages to the last client.
        running (bool): Flag indicating whether the server is running.

    Methods:
        receive_messages_from_clients: Receives messages from clients and responds to them.
        send_response_to_client: Sends response to the client and echoing the client message.
        send_user_message_to_last_client: Sends user input messages to the last connected client.
        run_server: Starts the server, listens for incoming messages, and handles client connections.
        stop_server: Stops the server and performs cleanup.
    """

    def __init__(self) -> None:
        """Initialize the server."""
        self.last_client_address: tuple = None
        self.lock: threading.Lock = threading.Lock()
        self.server_socket: socket.socket = None
        self.receiver_thread: threading.Thread = None
        self.user_thread: threading.Thread = None
        self.running: bool = False

    def receive_messages_from_clients(self) -> None:
        """Receive messages from clients and respond to them."""
        while self.running:
            try:
                message, client_address = self.server_socket.recvfrom(1024)
                print(f"\nReceived message from {client_address}: {message.decode()}")
                sys.stdout.flush()
                with self.lock:
                    self.last_client_address = client_address
                self.send_response_to_client(message, client_address)

            except socket.timeout:
                pass
            except socket.error as socket_error:
                print(f"Socket error: {socket_error}")
            except Exception as general_error:
                print(f"Failed to recieve message: {general_error}")

    def send_response_to_client(self, message: str, client_address: tuple) -> None:
        """Send response to the client and echoing the client message.
        Args:
           message (str): The message to send to the client.
           client_address (tuple): The address of the client.
        """
        try:
            self.server_socket.sendto(
                f"Echo: {message.decode()}".encode(), client_address
            )
        except socket.error as socket_error:
            print(f"Socket error in send_response_to_client: {socket_error}")
        except Exception as general_error:
            print(f"Failed to respond to the client message: {general_error}")

    def send_user_message_to_last_client(self) -> None:
        """Send user input messages to the last connected client.

        This method continuously prompts the user for input messages and sends
        them to the last connected client. It terminates when the user inputs
        'q' or 'quit'.

        """
        while self.running:
            if self.last_client_address is not None:
                message = input("message to the last client ( 'quit' or 'q' to stop): ")
                sys.stdout.flush()
                if message.lower() in ["quit", "q"]:
                    server.stop_server()
                    sys.exit(0)
                try:
                    self.server_socket.sendto(
                        f"Server user message: {message}".encode(),
                        self.last_client_address,
                    )
                except socket.error as socket_error:
                    print(
                        f"Socket error in send_user_message_to_last_client: {socket_error}"
                    )
                except Exception as general_error:
                    print(
                        f"Failed to send message to the last known client: {general_error}"
                    )

    def run_server(self, host: str, port: int) -> None:
        """Starts the server, listens for incoming messages, and handles clients connections.

        Args:
            host (str): The server's host address.
            port (int): The port number for listening.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind((host, port))
            self.server_socket.settimeout(1)
            self.running = True

            print(f"Server listening on {host}:{port}")

            self.receiver_thread = threading.Thread(
                target=self.receive_messages_from_clients
            )
            self.receiver_thread.start()

            self.user_thread = threading.Thread(
                target=self.send_user_message_to_last_client
            )
            self.user_thread.start()

            # Wait for KeyboardInterrupt to stop the server
            while self.running:
                time.sleep(1)

        except socket.error as socket_error:
            print(f"Socket error in run_server: {socket_error}")
            self.stop_server()
        except Exception as general_error:
            print(f"Failed to run the server properly: {general_error}")
            self.stop_server()
        finally:
            self.stop_server()

    def stop_server(self) -> None:
        """Stop the server and perform cleanup.

        This method stops the server and performs necessary cleanup tasks, including closing the
        server socket and joining the receiver and user threads."""
        if self.running:
            print("Server stopping...")
            self.running = False
            try:
                if threading.current_thread() != self.receiver_thread:
                    self.receiver_thread.join()
                if threading.current_thread() != self.user_thread:
                    self.user_thread.join()
                if self.server_socket:
                    self.server_socket.close()
                print("Server stopped.")
            except socket.error as socket_error:
                print(f"failed to close the socket: {socket_error}")
            except Exception as general_exception:
                print(f"failed to stop the server gracefully: {general_exception}")


if __name__ == "__main__":
    server = UDPServer()
    try:
        server.run_server("localhost", 12345)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Server shutting down...")
        sys.exit(0)
