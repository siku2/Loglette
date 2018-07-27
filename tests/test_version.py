from loglette import Version


def test_comp():
    v1 = Version(1, 5, 3)
    v2 = Version(1, 5, 2, tag="dev")
    assert v1 > v2
    assert v1 >= v2
    assert v1 != v2
    assert not (v1 < v2)
    assert v2 <= v1
    assert v2 == (1, 5, 2)
    assert v2 > (1, 0)
    assert v1 >= (1, 5, 3)
    assert v1 == (1, 5, 3, 0, 0, 0, 0)


def test_len():
    v = Version(2, 0, 0)
    v1 = Version(2)
    assert len(v) == 3
    assert len(v1) == 1


def test_str():
    assert str(Version(2, 1, 3)) == "2.1.3"
    assert str(Version(0, 0, 1, tag="dev")) == "0.0.1-dev"


def test_sem():
    assert Version(1, 0, 0).is_semantic
    assert not Version(2).is_semantic
    v = Version(9, 5, 7)
    assert v.major == 9
    assert v.minor == 5
    assert v.patch == 7


def test_parser():
    assert Version.parse("5.3") == Version(5, 3)
    assert Version.parse("2.5.5.5-no-sem") == Version(2, 5, 5, 5, tag="no-sem")


def test_code():
    assert Version(5, 3).version_code() == 5003
    assert Version(1, 3, 5).version_code(1) == 135
    assert Version().version_code(0) == 0
    v = Version(2, 0, 3)
    assert Version.parse(v.version_code()) == v
