from dfpy.steps.input import Input


class TimedGate(Input):
    """Outputs its input over a certain time interval, outputs 0 otherwise
    """
    def __init__(self, dimensions: list, min_time=0.0, max_time=None, name="TimedGate"):
        """Creates a TimedGate.

        :param min_time: the time at which the custom input should start
        :param max_time: the time at which the custom input should end (set to None if you want it to be there constantly)
        :param string name: name of the step
        """

        super().__init__(static=False, name=name)

        if type(dimensions) == tuple:
            dimensions = dimensions_from_sizes(*dimensions)

        self._dimensions = dimensions
        self._min_time = min_time
        self._max_time = max_time

        self._post_constructor()

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def min_time(self):
        return self._min_time

    @min_time.setter
    def min_time(self, min_time):
        self._min_time = min_time
        self._notify_observers()

    @property
    def max_time(self):
        return self._max_time

    @max_time.setter
    def max_time(self, max_time):
        self._max_time = max_time
        self._notify_observers()

    def shape(self):
        return tuple([dimension.size for dimension in self._dimensions])

    def dimensionality(self):
        return len(self._dimensions)
