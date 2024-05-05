import logging
import asyncio

from proxy import HttpReverseProxy, HttpProxyServer
from proxy.logger import ProxyLogger


# TODO transfer constants to .env
async def main():
    proxy_logger = ProxyLogger("proxy_logger")
    proxy = HttpReverseProxy("localhost", 8001, proxy_logger, buffer_size=4096, remote_address=b"localhost", remote_port=80)
    await proxy.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
