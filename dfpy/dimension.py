class Dimension:
    def __init__(self, lower: float, upper: float, size: int = None, name: str = "dim", ticklabels: dict = {}):
        """Creates a Dimension object that represents a field dimension.

        :param lower: lower bound of the domain
        :param upper: upper bound of the domain
        :param size: size of the array that holds the simulated activation values
        :param name: name of the dimension (e.g., hue, x, y)
        :param ticklabels: if applicable, tick labels
        """

        if size is None:
            size = upper-lower
            #if size % 2 == 0:
            #    size = size+1

        if size % 2 == 0:
            RuntimeWarning("It is recommended to provide an odd size for the dimensions. This avoids incompatibilities between different simulation frameworks.")


        if type(lower) == int:
            lower = float(lower)

        if type(upper) == int:
            upper = float(upper)

        assert type(size) == int, "size must be an int"
        assert type(lower) == float, "lower bound must be a float"
        assert type(upper) == float, "upper bound must be a float"
        assert type(ticklabels) == dict, "ticklabels bound must be a dict"

        self._lower = lower
        self._upper = upper
        self._size = size
        self._name = name
        self._ticklabels = ticklabels

    @classmethod
    def from_size(cls, size):
        return cls(lower=0.0, upper=float(size-1), size=size)

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

    @property
    def ticklabels(self):
        return self._ticklabels


def dimensions_from_sizes(*sizes):
    return [Dimension.from_size(size) for size in sizes]


def shape_from_list_of_dimensions(dimensions):
    return [dimension.size for dimension in dimensions]

