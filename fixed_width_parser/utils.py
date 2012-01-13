from itertools import islice, tee, izip

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    iterable = iter(iterable)
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def iterskip(iterator, test, n):
    """Iterate skipping values matching test, and n following values"""
    iterator = iter(iterator)
    while 1:
        value = next(iterator)
        if test(value):
            for dummy in range(n):
                next(iterator)
        else:
            yield value

def iterchunks(iterator, n):
    """Iterate returning n results at a time"""
    iterator = iter(iterator)
    return izip(*([iterator]*n))