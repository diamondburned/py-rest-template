from sonyflake import SonyFlake


_idGenerator = SonyFlake()
assert _idGenerator is not None


def generate_id() -> int:
    """
    This function generates a unique Snowflake ID.
    """
    return _idGenerator.next_id()
