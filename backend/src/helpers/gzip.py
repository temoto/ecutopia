from gzip import GzipFile
import io
import zlib


def gzip_string(s, level=6):
    """Compress string using gzip.
    Default compression level is 6.
    """
    zbuf = io.BytesIO()
    zfile = GzipFile(mode='wb', compresslevel=level, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    return zbuf.getvalue()


def gunzip_string(s):
    """Decompress string using gzip.

    See http://stackoverflow.com/questions/2695152/in-python-how-do-i-decode-gzip-encoding/2695466#2695466
    """
    return zlib.decompress(s, 16 + zlib.MAX_WBITS)
