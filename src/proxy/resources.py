import logging




class HTTPStatus:
    HTTP_200 = b"HTTP/1.1 200 Connection established\r\n\r\n"
    HTTP_301 = b"HTTP/1.1 301 Moved Permanently\r\n\r\n"
    HTTP_302 = b"HTTP/1.1 302 Found\r\n\r\n"
    HTTP_303 = b"HTTP/1.1 303 See Other\r\n\r\n"
    HTTP_307 = b"HTTP/1.1 307 Temporary Redirect\r\n\r\n"
    HTTP_308 = b"HTTP/1.1 308 Permanent Redirect\r\n\r\n"
    HTTP_400 = b"HTTP/1.1 400 Bad Request\r\n\r\n"
    HTTP_401 = b"HTTP/1.1 401 Unauthorized\r\n\r\n"
    HTTP_403 = b"HTTP/1.1 403 Forbidden\r\n\r\n"
    HTTP_404 = b"HTTP/1.1 404 Not Found\r\n\r\n"
    HTTP_405 = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    HTTP_407 = b"HTTP/1.1 407 Proxy Authentication Required\r\n\r\n"
    HTTP_408 = b"HTTP/1.1 408 Request Timeout\r\n\r\n"
    HTTP_429 = b"HTTP/1.1 429 Too Many Requests\r\n\r\n"
    HTTP_500 = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
    HTTP_501 = b"HTTP/1.1 501 Not Implemented\r\n\r\n"
    HTTP_502 = b"HTTP/1.1 502 Bad Gateway\r\n\r\n"
    HTTP_503 = b"HTTP/1.1 503 Service Unavailable\r\n\r\n"
    HTTP_504 = b"HTTP/1.1 504 Gateway Timeout\r\n\r\n"
