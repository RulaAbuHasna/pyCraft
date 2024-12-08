import pytest
from utils.paginator.dict_paginator import DictPaginator, paginate_dict, CustomCursorEncoder, DefaultCursorEncoder

def test_dict_paginator_basic():
    data = {"a": 1, "b": 2, "c": 3, "d": 4}
    paginator = DictPaginator(data, first=2)
    assert list(paginator.page.keys()) == ["a", "b"]
    assert paginator.has_next
    assert not paginator.has_previous

def test_dict_paginator_after():
    data = {"a": 1, "b": 2, "c": 3, "d": 4}
    paginator = DictPaginator(data, first=2, after="b")
    assert list(paginator.page.keys()) == ["c", "d"]
    assert not paginator.has_next
    assert paginator.has_previous

def test_dict_paginator_before():
    data = {"a": 1, "b": 2, "c": 3, "d": 4}
    paginator = DictPaginator(data, last=2, before="c")
    assert list(paginator.page.keys()) == ["a", "b"]
    assert paginator.has_next
    assert not paginator.has_previous

def test_dict_connection():
    data = {"a": 1, "b": 2, "c": 3}
    connection = paginate_dict(data, first=2)
    
    assert connection.total_count == 3
    assert len(connection.edges) == 2
    
    page_info = connection.page_info
    assert page_info["has_next_page"]
    assert not page_info["has_previous_page"]
    assert page_info["start_cursor"] == "a"
    assert page_info["end_cursor"] == "b"

def test_custom_cursor_encoder():
    def encode(x): return f"enc_{x}"
    def decode(x): return x[4:]
    
    encoder = CustomCursorEncoder(encode, decode)
    data = {"a": 1, "b": 2, "c": 3}
    connection = paginate_dict(data, first=2, encode_cursor=True, cursor_encoder=encoder)
    
    edges = connection.edges
    assert edges[0]["cursor"] == "enc_a"
    assert edges[1]["cursor"] == "enc_b"

def test_invalid_cursor():
    data = {"a": 1, "b": 2, "c": 3}
    with pytest.raises(ValueError):
        DictPaginator(data, after="invalid_cursor")

def test_first_and_last_error():
    data = {"a": 1, "b": 2, "c": 3}
    with pytest.raises(ValueError):
        DictPaginator(data, first=2, last=2)

def test_empty_page():
    data = {}
    connection = paginate_dict(data)
    assert connection.edges == []
    assert connection.page_info["start_cursor"] is None
    assert connection.page_info["end_cursor"] is None

def test_using_encoded_cursor_with_paginate_dict():
    data = {"a": 1, "b": 2, "c": 3, "d": 4}
    connection = paginate_dict(data, first=2, encode_cursor=True)
    cursor = connection.page_info["end_cursor"]
    connection = paginate_dict(data, after=cursor, first=2, encode_cursor=True)
    assert connection.paginator.page == {"c": 3, "d": 4}

def test_cursor_is_decoded():
    encoder = DefaultCursorEncoder()
    cursor = encoder.encode("a")
    assert encoder.decode(cursor) == "a"

def test_using_encoded_cursor_with_random_data_paginate_dict():
    data = {"a": "leo", "b": "is", "c": "a", "d": "beautiful", "e": "cat"}
    connection = paginate_dict(data, first=3, encode_cursor=True)
    cursor = connection.page_info["end_cursor"]
    connection = paginate_dict(data, after=cursor, first=2, encode_cursor=True)
    assert connection.paginator.page == {"d": "beautiful", "e": "cat"}
