from dfpy.steps.step import Step


class TimedBoost(Step):
    """Computes a piecewise scalar function of time.
    """
    def __init__(self, values: dict={0: 0}, name: str = "Boost"):
        """Creates a piecewise scalar function.

        :param values: dictionary mapping points in time to values of the function (at any time step t, the value
        of the function will correspond to the last specified value before t)
        :param name: name of the step
        """

        super().__init__(name=name)

        self._values = {}
        for key in values:
            self._values[float(key)] = float(values[key])

        self._post_constructor()

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = values
        self._notify_observers("values")
