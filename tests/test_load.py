from .bytes import get_code


def test_code_load():
    code = get_code()
    def x():
        pass
    x.__code__ = code
    assert x() == 3  # Lololol.
