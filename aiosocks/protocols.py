import asyncio
import socket
import struct
from asyncio import sslproto

from . import constants as c
from .helpers import (
    Socks4Addr, Socks5Addr, Socks5Auth, Socks4Auth
)
from .errors import (
    SocksError, NoAcceptableAuthMethods, LoginAuthenticationFailed,
    InvalidServerReply, InvalidServerVersion
)


DEFAULT_LIMIT = getattr(asyncio.streams, '_DEFAULT_LIMIT', 2**16)


class BaseSocksProtocol(asyncio.StreamReaderProtocol):
    def __init__(self, proxy, proxy_auth, dst, app_protocol_factory, waiter, *,
                 remote_resolve=True, loop=None, ssl=False,
                 server_hostname=None, negotiate_done_cb=None,
                 reader_limit=DEFAULT_LIMIT):
        if not isinstance(dst, (tuple, list)) or len(dst) != 2:
            raise ValueError(
                'Invalid dst format, tuple("dst_host", dst_port))'
            )

        self._proxy = proxy
        self._auth = proxy_auth
        self._dst_host, self._dst_port = dst
        self._remote_resolve = remote_resolve
        self._waiter = waiter
        self._ssl = ssl
        self._server_hostname = server_hostname
        self._negotiate_done_cb = negotiate_done_cb
        self._loop = loop or asyncio.get_event_loop()

        self._transport = None
        self._negotiate_done = False
        self._proxy_peername = None
        self._proxy_sockname = None

        if app_protocol_factory:
            self._app_protocol = app_protocol_factory()
        else:
            self._app_protocol = self

        reader = asyncio.StreamReader(loop=self._loop, limit=reader_limit)

        super().__init__(stream_reader=reader,
                         client_connected_cb=self.negotiate, loop=self._loop)

    async def negotiate(self, reader, writer):
        pass

    def connection_made(self, transport):
        # connection_made is called
        pass

    def connection_lost(self, exc):
        pass

    def pause_writing(self):
        pass

    def resume_writing(self):
        pass

    def data_received(self, data):
        pass

    def eof_received(self):
        pass

    async def socks_request(self, cmd):
        raise NotImplementedError

    def write_request(self, request):
        pass

    async def read_response(self, n):
        pass

    async def _get_dst_addr(self):
        pass

    @property
    def app_protocol(self):
        pass

    @property
    def app_transport(self):
        pass

    @property
    def proxy_sockname(self):
        """
        Returns the bound IP address and port number at the proxy.
        """
        pass

    @property
    def proxy_peername(self):
        """
        Returns the IP and port number of the proxy.
        """
        pass

    @property
    def peername(self):
        """
        Returns the IP address and port number of the destination
        machine (note: get_proxy_peername returns the proxy)
        """
        pass

    @property
    def reader(self):
        pass

    @property
    def writer(self):
        pass


class Socks4Protocol(BaseSocksProtocol):
    def __init__(self, proxy, proxy_auth, dst, app_protocol_factory, waiter,
                 remote_resolve=True, loop=None, ssl=False,
                 server_hostname=None, negotiate_done_cb=None,
                 reader_limit=DEFAULT_LIMIT):
        proxy_auth = proxy_auth or Socks4Auth('')

        if not isinstance(proxy, Socks4Addr):
            raise ValueError('Invalid proxy format')

        if not isinstance(proxy_auth, Socks4Auth):
            raise ValueError('Invalid proxy_auth format')

        super().__init__(proxy, proxy_auth, dst, app_protocol_factory,
                         waiter, remote_resolve=remote_resolve, loop=loop,
                         ssl=ssl, server_hostname=server_hostname,
                         reader_limit=reader_limit,
                         negotiate_done_cb=negotiate_done_cb)

    async def socks_request(self, cmd):
        # prepare destination addr/port
        pass


class Socks5Protocol(BaseSocksProtocol):
    def __init__(self, proxy, proxy_auth, dst, app_protocol_factory, waiter,
                 remote_resolve=True, loop=None, ssl=False,
                 server_hostname=None, negotiate_done_cb=None,
                 reader_limit=DEFAULT_LIMIT):
        proxy_auth = proxy_auth or Socks5Auth('', '')

        if not isinstance(proxy, Socks5Addr):
            raise ValueError('Invalid proxy format')

        if not isinstance(proxy_auth, Socks5Auth):
            raise ValueError('Invalid proxy_auth format')

        super().__init__(proxy, proxy_auth, dst, app_protocol_factory,
                         waiter, remote_resolve=remote_resolve, loop=loop,
                         ssl=ssl, server_hostname=server_hostname,
                         reader_limit=reader_limit,
                         negotiate_done_cb=negotiate_done_cb)

    async def socks_request(self, cmd):
        pass

    async def authenticate(self):
        # send available auth methods
        pass

    async def build_dst_address(self, host, port):
        pass

    async def read_address(self):
        pass
