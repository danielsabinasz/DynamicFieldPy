from dfpy.steps.step import Step


class Boost(Step):
    """Computes a piecewise scalar function of time.
    """
    def __init__(self, value: float, name: str = "Boost"):
        """Creates a piecewise scalar function.

        :param value: value of the boost
        :param name: name of the step
        """

        super().__init__(name=name)

        self._value = float(value)

        self._post_constructor()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._notify_observers("value")

    def dimensionality(self):
        return 0

