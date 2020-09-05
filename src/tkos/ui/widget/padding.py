class Padding(object):
    """A class for specifying inner padding of Widgets."""
    def __init__(self, l:int, t:int, r:int, b:int):
        """Creates a generic padding.

        Args:
            l (int): Left padding.
            t (int): Top padding.
            r (int): Right padding.
            b (int): Bottom padding.
        """
        self.pad_left = l
        self.pad_top = t
        self.pad_right = r
        self.pad_bottom = b

    @classmethod
    def symmetric(cls, hor:int, ver:int):
        """Creates a symmetric padding.

        Args:
            hor (int): The horizontal padding.
            ver (int): The vertical padding.

        Returns:
            Padding: The generated padding.
        """
        return cls(hor, ver, hor, ver)

    @classmethod
    def small(cls):
        """A default small padding of 8 pixels.

        Returns:
            Padding: The generated padding.
        """
        return cls.symmetric(8, 8)

    @classmethod
    def medium(cls):
        """A default medium padding of 24 pixels.

        Returns:
            Padding: The generated padding.
        """
        return cls.symmetric(24, 24)

    @classmethod
    def large(cls):
        """A default large padding of 40 pixels.

        Returns:
            Padding: The generated padding.
        """
        return cls.symmetric(40, 40)
