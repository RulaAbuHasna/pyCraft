from typing import Any, Dict, List, Optional, Callable
import os

PYCRAFT_PAGINATOR_SECRET=os.getenv("PYCRAFT_PAGINATOR_SECRET")

class DefaultCursorEncoder:
    """Default cursor encoder using simple string conversion of indexes with encryption."""
    def __init__(self, secret: str = PYCRAFT_PAGINATOR_SECRET):
        self.secret = secret
        
    def encode(self, position: int) -> str:
        # XOR with secret bytes for simple reversible encryption
        key = int.from_bytes(self.secret.encode(), 'big') 
        encoded = position ^ key
        return f"{position}:{encoded}"

    def decode(self, cursor: str) -> int:
        # Split cursor into original and encrypted parts
        original, encrypted = cursor.split(':')
        key = int.from_bytes(self.secret.encode(), 'big')
        if int(original) ^ key != int(encrypted):
            raise ValueError("Invalid cursor - encryption verification failed")
        return int(original)


class CustomCursorEncoder:
    """Custom cursor encoder with user-defined encode/decode functions."""
    def __init__(
        self, 
        encode_func: Callable[[int], str], 
        decode_func: Callable[[str], int]
    ):
        self._encode = encode_func
        self._decode = decode_func

    def encode(self, position: int) -> str:
        return self._encode(position)

    def decode(self, cursor: str) -> int:
        return self._decode(cursor)


class ArrayPaginator:
    """Cursor-based paginator for in-memory arrays."""
    def __init__(
        self,
        data: List[Any],
        first: Optional[int] = None,
        last: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        encode_cursor: bool = False,
        cursor_encoder: Optional[CustomCursorEncoder] = None,
    ):
        self.data = data
        self.start_index = 0
        self.end_index = len(data)

        # Default encoder behavior: no encoding/decoding
        if not encode_cursor:
            self.cursor_encoder = None
            self._encode = str
            self._decode = int
        else:
            self.cursor_encoder = cursor_encoder or DefaultCursorEncoder()
            self._encode = self.cursor_encoder.encode
            self._decode = self.cursor_encoder.decode

        # Validate first/last input
        if first and last:
            raise ValueError("Cannot provide both 'first' and 'last'")

        # Handle 'after' cursor
        if after is not None:
            self.start_index = self._decode(after) + 1

        # Handle 'before' cursor
        if before is not None:
            self.end_index = min(self.end_index, self._decode(before))

        # Ensure valid bounds
        self.start_index = max(self.start_index, 0)
        self.end_index = min(self.end_index, len(data))

        # Apply first/last pagination
        if first is not None:
            self.end_index = min(self.start_index + first, len(data))
        if last is not None:
            range_length = self.end_index - self.start_index
            if range_length > last:
                self.start_index = self.end_index - last

    def cursor(self, position: int) -> str:
        """Generate a cursor based on the position."""
        return self._encode(position)

    @property
    def page(self) -> List[Any]:
        """Returns the sliced page of data."""
        return self.data[self.start_index : self.end_index]

    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.end_index < len(self.data)

    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.start_index > 0


class ArrayConnection:
    """Connection wrapper for array pagination."""
    def __init__(self, data: List[Any], paginator: ArrayPaginator):
        self.data = data
        self.paginator = paginator

    @property
    def edges(self) -> List[Dict[str, Any]]:
        return [
            {"cursor": self.paginator.cursor(self.paginator.start_index + i), "node": node}
            for i, node in enumerate(self.paginator.page)
        ]

    @property
    def total_count(self) -> int:
        return len(self.data)

    @property
    def page_info(self) -> Dict[str, Any]:
        return {
            "has_next_page": self.paginator.has_next,
            "has_previous_page": self.paginator.has_previous,
            "start_cursor": self.paginator.cursor(self.paginator.start_index) if self.paginator.page else None,
            "end_cursor": self.paginator.cursor(self.paginator.end_index - 1) if self.paginator.page else None,
        }


def paginate_array(
    data: List[Any],
    encode_cursor: bool = False,
    cursor_encoder: Optional[CustomCursorEncoder] = None,
    **kwargs
) -> ArrayConnection:
    """
    Paginate an array of data.
    
    Args:
        data: List to paginate
        encode_cursor: Whether to use cursor encoding/decoding (default: False)
        cursor_encoder: Custom encoder for encoding/decoding cursors (optional)
        **kwargs: Pagination parameters (first, last, after, before)
    
    Returns:
        Paginated array connection.
    """
    paginator = ArrayPaginator(
        data, encode_cursor=encode_cursor, cursor_encoder=cursor_encoder, **kwargs
    )
    return ArrayConnection(data, paginator)
