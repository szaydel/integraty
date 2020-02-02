import sys

from integraty import xstring


class TestString:

    def test_skip_lines(self):
        lines = \
            """alpha
            beta
            gamma
            delta
            epsilon"""
        xs = xstring.String(lines)
        assert xs.skip_lines(skip_head=1) \
            == ['beta', 'gamma', 'delta', 'epsilon']
        assert xs.skip_lines(skip_tail=1) \
            == ['alpha', 'beta', 'gamma', 'delta']
        assert xs.skip_lines(skip_head=1, skip_tail=1) \
            == ['beta', 'gamma', 'delta']
        assert xs.skip_lines(skip_tail=1, pattern="alpha") \
            == []
        assert xs.skip_lines(skip_head=1, pattern="(alpha|gamma)") \
            == ['gamma']
        assert xs.skip_lines(skip_head=1, skip_tail=1,
        pattern="(alpha|beta|gamma)") \
            == ['beta']
        assert xs.skip_lines(skip_tail=1, pattern="alpha", exclude=True) \
            == ['beta', 'gamma', 'delta']
        assert xs.skip_lines(skip_head=1, pattern="alpha", exclude=True) \
            == ['gamma', 'delta', 'epsilon']
