from etl.transform import to_float

def test_to_float():
    assert to_float(1) == 1.0
    assert to_float('5') == 5.0
    assert to_float('hello') is None
    assert to_float(None) is None