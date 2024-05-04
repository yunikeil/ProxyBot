import asyncio
import logging

from .resources import HTTPStatus
from .core import AsyncioSocket, ProxyListener


class ProxyServer: # Only HTTP now
    def __init__(self, ip_address: str, port: int, buffer_size: int, logger: logging.Logger) -> None:
        self.__ip_address = ip_address
        self.__port = port
        self.__buffer_size = buffer_size
        self.__server = None
        self.logger = logger

    @property
    def server_address(self):
        return self.__server.sockets[0].getsockname()
    
    async def new_client_callback(
        self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter
    ):
        try:
            client_socket = AsyncioSocket(reader, writer, self.__buffer_size)
            request_data = await client_socket.read()
            method, address, _ = request_data.splitlines()[0].split()
            client_address = client_socket.writer.get_extra_info("peername")

            self.logger.info(
                f"New connection from client\t{client_address[0]}:{client_address[1]}"
            )
            
            if method == b"CONNECT":
                remote_socket = await AsyncioSocket.open_connection(
                    *address.split(b":"), self.__buffer_size, self.logger
                )
                client_socket.write(HTTPStatus.HTTP_200)
                await client_socket.drain()

            else:
                remote_socket: AsyncioSocket = await AsyncioSocket.open_connection(
                    address, 80, self.__buffer_size, self.logger
                )
                remote_socket.write(request_data)
                await remote_socket.drain()

            listener = ProxyListener(client_socket, remote_socket, self.logger)
            self.logger.debug(f"Count listeners: {len(ProxyListener.listeners)}")

            await listener.start_proxy()

        except (AttributeError, ValueError, LookupError):
            # cant read client data to connect
            client_socket.write(HTTPStatus.HTTP_400)
            await client_socket.drain()
            await client_socket.close()

            return

        except TimeoutError:
            await client_socket.private_close()

        except ConnectionRefusedError:
            # cant connect to remote socket
            client_socket.write(HTTPStatus.HTTP_403)
            await client_socket.drain()
            await client_socket.close()

            return

        except BaseException as ex:
            self.logger.exception(ex)
            self.logger.error(request_data)

            return

    async def serve_forever(self):
        if self.__server is not None:
            raise ValueError("Server already started")

        self.__server = await asyncio.start_server(
            self.new_client_callback, self.__ip_address, self.__port
        )

        self.logger.info(f"Server started at {self.server_address}")

        async with self.__server:
            await self.__server.serve_forever()
