import logging
import asyncio

from proxy import ProxyServer
from proxy.logger import ProxyLogger


# TODO transfer constants to .env
async def main():
    proxy_logger = ProxyLogger("proxy_logger")
    proxy = ProxyServer("localhost", 8000, 4096, proxy_logger)
    await proxy.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
