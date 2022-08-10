from dfpy.steps.step import Step


class Scalar(Step):
    """Computes/yields a scalar.
    """
    def __init__(self, value=1.0, name="Scalar"):
        """Creates a scalar.

        :param float value: the value of the scalar
        :param string name: name of the step
        """

        super().__init__(static=True, name=name)

        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
