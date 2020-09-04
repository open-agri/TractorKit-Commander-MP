class Padding(object):
    def __init__(self, l, t, r, b):
        self.pad_left = l
        self.pad_top = t
        self.pad_right = r
        self.pad_bottom = b
    
    @classmethod
    def symmetric(cls, hor, ver):
        return cls(hor, ver, hor, ver)

    @classmethod
    def small(cls):
        return cls.symmetric(8, 8)

    @classmethod
    def medium(cls):
        return cls.symmetric(24, 24)

    @classmethod
    def large(cls):
        return cls.symmetric(40, 40)