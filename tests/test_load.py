import dis
import io

from .bytes import get_code


def test_code_load():
    code = get_code()
    def x():
        pass
    x.__code__ = code
    assert x() == 3  # Lololol.


def test_code_unoptimized():
    code = get_code()
    stream = io.StringIO()
    dis.disco(code, file=stream)
    stream.seek(0)
    buf = stream.read()
    assert "0 LOAD_CONST               1 (1)" in buf
    assert "3 LOAD_CONST               2 (2)" in buf
