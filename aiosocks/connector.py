try:
    import aiohttp
    from aiohttp.client_exceptions import cert_errors, ssl_errors
except ImportError:  # pragma: no cover
    raise ImportError('aiosocks.SocksConnector require aiohttp library')

from .errors import SocksConnectionError
from .helpers import Socks4Auth, Socks5Auth, Socks4Addr, Socks5Addr
from . import create_connection

__all__ = ('ProxyConnector', 'ProxyClientRequest')


class ProxyClientRequest(aiohttp.ClientRequest):
    def update_proxy(self, proxy, proxy_auth, proxy_headers):
        pass


class ProxyConnector(aiohttp.TCPConnector):
    def __init__(self, remote_resolve=True, **kwargs):
        super().__init__(**kwargs)

        self._remote_resolve = remote_resolve

    async def _create_proxy_connection(self, req, *args, **kwargs):
        pass

    async def _wrap_create_socks_connection(self, *args, req, **kwargs):
        pass

    def _get_fingerprint_and_hashfunc(self, req):
        pass

    async def _create_socks_connection(self, req):
        pass
