from enum import Enum
from typing import *

from requests import get, post




__all__ = [
    'URL',
    'InternalRequest',
    ]


class URL(str):
    """ Any HTTP link """
    def __init__(self, url: str):
        if not isinstance(url, str): url = str(url)
        if not url.lower().strip().startswith('http'): raise ValueError(f'passed url is not a link: "{url}"')
        super().__init__(url)

    def Get(self, params: Union[Dict[str, str], List[str], Tuple[str, ...]] = None, **kwargs) -> bytes:
        """Sends a GET request.

        :param params: (optional) Dictionary, list of tuples or bytes to send in the query string for the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
                :data: (optional) Dictionary, list of tuples, bytes, or file-like
                    object to send in the body of the :class:`Request`.
                :json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
                :headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
                :cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
                :files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
                    ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
                    or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
                    defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
                    to add for the file.
                :auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
                :timeout: (optional) How many seconds to wait for the server to send data
                    before giving up, as a float, or a :ref:`(connect timeout, read
                    timeout) <timeouts>` tuple.
                :allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
                :proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
                :verify: (optional) Either a boolean, in which case it controls whether we verify the server's TLS certificate,
                                    or a string, in which case it must be a path to a CA bundle to use. Defaults to ``True``.
                :stream: (optional) if ``False``, the response content will be immediately downloaded.
                :cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        :return: content of the request.get response
        :rtype: bytes
        """
        return get(self, params, **kwargs).content

    def Post(self, data: Union[str, bytes, Dict, List] = None, json: Dict[str, Any] = None, **kwargs) -> bytes:
        """Sends a POST request.

        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
                :data: (optional) Dictionary, list of tuples, bytes, or file-like
                    object to send in the body of the :class:`Request`.
                :json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
                :headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
                :cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
                :files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
                    ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
                    or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
                    defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
                    to add for the file.
                :auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
                :timeout: (optional) How many seconds to wait for the server to send data
                    before giving up, as a float, or a :ref:`(connect timeout, read
                    timeout) <timeouts>` tuple.
                :allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
                :proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
                :verify: (optional) Either a boolean, in which case it controls whether we verify the server's TLS certificate,
                                    or a string, in which case it must be a path to a CA bundle to use. Defaults to ``True``.
                :stream: (optional) if ``False``, the response content will be immediately downloaded.
                :cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        :return: content of the request.get response
        :rtype: bytes
        """
        return post(self, data, json, **kwargs).content



_TAction = TypeVar('_TAction', Enum, str, int)
class InternalRequest(Generic[_TAction]):
    def __init__(self, action: _TAction, *args, **kwargs):
        self.Action: Final[_TAction] = action
        self.args: Final[Tuple] = args
        self.kwargs: Final[Dict[str, Any]] = kwargs
