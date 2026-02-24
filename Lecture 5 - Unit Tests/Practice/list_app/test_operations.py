from operations import get_last_item

def test_get_last_item_normal():
    assert get_last_item([1, 2, 3]) == 3

def test_get_last_item_empty():
    assert get_last_item([]) is None