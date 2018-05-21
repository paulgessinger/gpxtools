class Interval:
    def __init__(self, start, end):
        if start < end:
            self.start = start
            self.end = end
        else:
            self.start = end
            self.end = start

    def overlap(self, other):
        if self.start > other.start and self.start < other.end:
            return True

        if self.end > other.start and self.end < other.end:
            return True

        return False

    def __repr__(self):
        return "Interval(start={}, end={})".format(self.start, self.end)

    def __add__(self, other):
        return Interval(start=min(self.start, other.start), end=max(self.end, other.end))
