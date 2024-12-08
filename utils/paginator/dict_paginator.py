from typing import Any, Dict, List, Optional, Callable
from cryptography.fernet import Fernet

class DefaultCursorEncoder:
    """Default cursor encoder using simple string conversion of indexes with encryption."""
    def __init__(self, secret: str = Fernet.generate_key()):
        self.secret = Fernet(secret)

    def encode(self, position: str) -> str:
        """Encode the position using Fernet encryption."""
        position_bytes = position.encode('utf-8')
        encoded = self.secret.encrypt(position_bytes)
        return encoded.decode('utf-8')

    def decode(self, cursor: str) -> str:
        """Decode the cursor back to the original position."""
        cursor_bytes = cursor.encode('utf-8')
        decoded = self.secret.decrypt(cursor_bytes)
        return decoded.decode('utf-8')

class CustomCursorEncoder:
    """Custom cursor encoder with user-defined encode/decode functions."""
    def __init__(
        self,
        encode_func: Callable[[str], str],
        decode_func: Callable[[str], str]
    ):
        self._encode = encode_func
        self._decode = decode_func

    def encode(self, position: str) -> str:
        return self._encode(position)

    def decode(self, cursor: str) -> str:
        return self._decode(cursor)

class DictPaginator:
    """Cursor-based paginator for dictionaries."""
    def __init__(
        self,
        data: Dict[str, Any],
        first: Optional[int] = None,
        last: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        encode_cursor: bool = False,
        cursor_encoder: Optional[CustomCursorEncoder] = None,
    ):
        self.data = data
        self.keys = list(data.keys())
        self.start_index = 0
        self.end_index = len(self.keys)

        # Default encoder behavior: no encoding/decoding
        if not encode_cursor:
            self.cursor_encoder = None
            self._encode = str
            self._decode = str
        else:
            self.cursor_encoder = cursor_encoder or DefaultCursorEncoder()
            self._encode = self.cursor_encoder.encode
            self._decode = self.cursor_encoder.decode

        # Validate first/last input
        if first and last:
            raise ValueError("Cannot provide both 'first' and 'last'")

        # Handle 'after' cursor
        if after is not None:
            try:
                after_key = self._decode(after)
                self.start_index = self.keys.index(after_key) + 1
            except (ValueError, KeyError) as e:
                raise ValueError(f"Invalid cursor format: {after}") from e

        # Handle 'before' cursor
        if before is not None:
            try:
                before_key = self._decode(before)
                self.end_index = min(self.end_index, self.keys.index(before_key))
            except (ValueError, KeyError) as e:
                raise ValueError(f"Invalid cursor format: {before}") from e

        # Ensure valid bounds
        self.start_index = max(self.start_index, 0)
        self.end_index = min(self.end_index, len(self.keys))

        # Apply first/last pagination
        if first is not None:
            self.end_index = min(self.start_index + first, len(self.keys))
        if last is not None:
            range_length = self.end_index - self.start_index
            if range_length > last:
                self.start_index = self.end_index - last

    def cursor(self, key: str) -> str:
        """Generate a cursor based on the dictionary key."""
        return self._encode(key)

    @property
    def page(self) -> Dict[str, Any]:
        """Returns the sliced page of data."""
        return {
            k: self.data[k] 
            for k in self.keys[self.start_index:self.end_index]
        }

    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.end_index < len(self.keys)

    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.start_index > 0

class DictConnection:
    """Connection wrapper for dictionary pagination."""
    def __init__(self, data: Dict[str, Any], paginator: DictPaginator):
        self.data = data
        self.paginator = paginator

    @property
    def edges(self) -> List[Dict[str, Any]]:
        return [
            {
                "cursor": self.paginator.cursor(key),
                "node": {"key": key, "value": value}
            }
            for key, value in self.paginator.page.items()
        ]

    @property
    def total_count(self) -> int:
        return len(self.data)

    @property
    def page_info(self) -> Dict[str, Any]:
        page_keys = list(self.paginator.page.keys())
        return {
            "has_next_page": self.paginator.has_next,
            "has_previous_page": self.paginator.has_previous,
            "start_cursor": self.paginator.cursor(page_keys[0]) if page_keys else None,
            "end_cursor": self.paginator.cursor(page_keys[-1]) if page_keys else None,
        }

def paginate_dict(
    data: Dict[str, Any],
    encode_cursor: bool = False,
    cursor_encoder: Optional[CustomCursorEncoder] = None,
    **kwargs
) -> DictConnection:
    """
    Paginate a dictionary.
    
    Args:
        data: Dictionary to paginate
        encode_cursor: Whether to use cursor encoding/decoding (default: False)
        cursor_encoder: Custom encoder for encoding/decoding cursors (optional)
        **kwargs: Pagination parameters (first, last, after, before)
    
    Returns:
        Paginated dictionary connection.
    """
    paginator = DictPaginator(
        data, encode_cursor=encode_cursor, cursor_encoder=cursor_encoder, **kwargs
    )
    return DictConnection(data, paginator)
