from . import python


if python.PY3:
    def str_utf8(x):
        """
        Returns the byte string representation of obj.
        Like str(x).encode('utf-8') except it works for bytes.
        """
        if isinstance(x, str):
            return x
        return str(x).encode('utf-8')


    def from_utf8(x):
        """
        Returns the string representation of obj.
        Like str(x).decode('utf-8') except it works for bytes.
        """
        if isinstance(x, str):
            return x
        if isinstance(x, bytes):
            return x.decode('utf-8', 'replace')
        return str(x)
