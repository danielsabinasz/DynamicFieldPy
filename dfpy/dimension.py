class Dimension:
    def __init__(self, lower: float, upper: float, size: int, name: str = "dim"):
        """Creates a Dimension object that represents a field dimension.

        :param lower: lower bound of the domain
        :param upper: upper bound of the domain
        :param size: size of the array that holds the simulated activation values
        :param name: name of the dimension (e.g., hue, x, y)
        """

        if size % 2 == 0:
            raise RuntimeError("Please provide an odd size for the dimensions. This avoids incompatibilities between different simulation frameworks.")

        self._lower = lower
        self._upper = upper
        self._size = size
        self._name = name

    @classmethod
    def from_size(cls, size):
        return cls(lower=0, upper=size-1, size=size)

    @property
    def name(self):
        return self._name

    @property
    def lower(self):
        return self._lower

    @property
    def upper(self):
        return self._upper

    @property
    def size(self):
        return self._size


def dimensions_from_sizes(sizes):
    return [Dimension.from_size(size) for size in sizes]
