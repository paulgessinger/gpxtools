from datetime import datetime

from gpxutil.util import Interval

def test_interval():
    # no overlap
    int_a = Interval(datetime(2018, 5, 21, 10), datetime(2018, 5, 21, 14))
    int_b = Interval(datetime(2018, 5, 21, 15), datetime(2018, 5, 21, 18))

    assert not int_a.overlap(int_b)
    assert not int_b.overlap(int_a)

    # overlap
    int_a = Interval(datetime(2018, 5, 21, 10), datetime(2018, 5, 21, 15))
    int_b = Interval(datetime(2018, 5, 21, 14), datetime(2018, 5, 21, 18))

    assert int_a.overlap(int_b)
    assert int_b.overlap(int_a)

    int_a = Interval(datetime(2018, 5, 21, 10), datetime(2018, 5, 21, 14))
    int_b = Interval(datetime(2018, 5, 21, 15), datetime(2018, 5, 21, 18))

    int_c = int_a + int_b
    assert int_c.start == int_a.start
    assert int_c.end == int_b.end
    
    int_d = int_b + int_a
    assert int_d.start == int_a.start
    assert int_d.end == int_b.end

