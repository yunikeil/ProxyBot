import asyncio
import logging
from urllib.parse import urlparse


class AsyncioSocket:
    sockets: list["AsyncioSocket"] = []

    def __init__(
        self,
        reader: asyncio.streams.StreamReader,
        writer: asyncio.streams.StreamWriter,
        buffer_size: int,
    ) -> None:
        self.reader: asyncio.streams.StreamReader = reader
        self.writer: asyncio.streams.StreamWriter = writer
        self.buffer_size = buffer_size
        self.sockets.append(self)

    @staticmethod
    async def open_connection(
        host: bytes,
        port: int | str,
        buffer_size: int,
        logger: logging.Logger,
    ) -> "AsyncioSocket":
        if not (host_ := urlparse(host.decode()).hostname):
            host_ = urlparse(host.decode()).path

        reader, writer = await asyncio.open_connection(host_, int(port))
        logger.info(f"New connection to remote {host_}:{int(port)}")
        logger.debug(f"Count sockets: {len(AsyncioSocket.sockets) + 1}")
        
        return AsyncioSocket(reader, writer, buffer_size)

    async def read_untill(self, sep: bytes):
        data = await self.reader.readuntil(sep)
        return data

    async def read(self):
        try:
            data = await asyncio.wait_for(self.reader.read(self.buffer_size), 0.1)
            return data
        except asyncio.exceptions.TimeoutError:
            return None

    def write(self, data: bytes):
        self.writer.write(data)

    async def drain(self):
        await self.writer.drain()

    def private_close(self):
        self.writer.close()
        self.sockets.remove(self)

    async def close(self):
        self.write(b"")
        await self.drain()
        self.private_close()


class ProxyListener:
    listeners: list["ProxyListener"] = []

    def __init__(
        self, client: AsyncioSocket, remote: AsyncioSocket, logger: logging.Logger
    ) -> None:
        self.client = client
        self.remote = remote
        self.logging = logger
        self.not_data_count: int = 0
        self.socket_waiting_s: int = 10
        self.not_data_timeout: int = 0.001
        self.started: bool = False
        self.listeners.append(self)

    @classmethod
    async def stop_all(cls):
        for l in cls.listeners:
            await l.stop_proxy()

    async def stop_proxy(self, is_private: bool = False):
        if not self.started:
            return

        if is_private:
            self.remote.private_close()
            self.client.private_close()

        else:
            await self.remote.close()
            await self.client.close()

        self.listeners.remove(self)
        self.started = False

    def check_is_connections_empty(self):
        if self.not_data_count > (self.socket_waiting_s / self.not_data_timeout):
            return True
        return False

    async def transfer_data(self, sender: AsyncioSocket, receiver: AsyncioSocket):
        while True:
            data = await sender.read()

            if self.check_is_connections_empty():
                await self.stop_proxy()
                return

            if not data:
                self.not_data_count += 1
                await asyncio.sleep(self.not_data_timeout)
                continue

            self.not_data_count = 0
            receiver.write(data)
            await receiver.drain()

    async def start_transfer_to_client(self):
        await self.transfer_data(self.remote, self.client)

    async def start_transfer_to_server(self):
        await self.transfer_data(self.client, self.remote)

    async def start_proxy(self):
        self.started = True
        tasks = [self.start_transfer_to_client(), self.start_transfer_to_server()]

        try:
            await asyncio.gather(*tasks)

        except BrokenPipeError:
            await self.stop_proxy(is_private=True)

        except ConnectionResetError:
            await self.stop_proxy(is_private=True)
