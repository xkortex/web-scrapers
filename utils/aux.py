
def lazyparse(value):
    """
    This function will try very hard to coerce the value.
    If it can't, it'll cowardly give up without an exception and return the original value.
    Life is short, use fast-and-loose parsers.
    :param value:
    :type value: str
    :return: Coerced value, or original string
    >>> lazyparse('')
    ''
    >>> lazyparse('3')
    3
    >>> type(lazyparse('3'))
    <class 'int'>
    """
    value = value.lower()
    if value in ['yes', 'true', 'on', 'y']:
        return True
    if value in ['no', 'false', 'off', 'n']:
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value