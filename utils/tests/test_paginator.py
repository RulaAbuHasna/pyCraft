import pytest
from utils.paginator import ArrayPaginator, paginate_array

@pytest.fixture
def items():
    return list(range(1, 101))

def test_page_content(items):
    paginator = ArrayPaginator(items, first=10)
    assert paginator.page == list(range(1, 11))

def test_has_next(items):
    paginator = ArrayPaginator(items, first=10)
    assert paginator.has_next

def test_has_previous(items):
    paginator = ArrayPaginator(items, first=10)
    assert not paginator.has_previous

def test_pagination_with_after(items):
    paginator = ArrayPaginator(items, after="5:6", first=5)
    assert paginator.page == list(range(7, 12))

def test_pagination_with_before(items):
    paginator = ArrayPaginator(items, before="10:11", last=5)
    assert paginator.page == list(range(6, 11))

def test_invalid_after_cursor(items):
    with pytest.raises(ValueError):
        ArrayPaginator(items, after="invalid_cursor")

def test_invalid_before_cursor(items):
    with pytest.raises(ValueError):
        ArrayPaginator(items, before="invalid_cursor")

def test_empty_array():
    paginator = ArrayPaginator([], first=10)
    assert paginator.page == []
    assert not paginator.has_next
    assert not paginator.has_previous

def test_fewer_items_than_page_size():
    paginator = ArrayPaginator([1, 2, 3], first=10)
    assert paginator.page == [1, 2, 3]
    assert not paginator.has_next
    assert not paginator.has_previous

def test_last_parameter(items):
    paginator = ArrayPaginator(items, last=5)
    assert paginator.page == list(range(96, 101))
    assert not paginator.has_next
    assert paginator.has_previous

def test_first_and_last_conflict(items):
    with pytest.raises(ValueError):
        ArrayPaginator(items, first=10, last=5)

def test_paginate_array_function(items):
    connection = paginate_array(items, first=10)
    assert connection.paginator.page == list(range(1, 11))
    assert connection.total_count == 100
