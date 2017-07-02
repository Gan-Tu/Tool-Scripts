def flatten(lst):
    def helper(myseq):
        """Lazily flatten a given sequence."""
        for x in myseq:
            if isinstance(x, (list, tuple, set, dict)):
                yield from flatten(x)
            else:
                yield x
    return list(helper(lst))
