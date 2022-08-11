from dfpy.steps.step import Step


class ScalarMultiplication(Step):
    """Computes a multiplication of its input with a scalar.
    """
    def __init__(self, shape, scalar=1.0, name="Scalar Multiplication"):
        """Creates a scalar multiplication.

        :param float value: the value of the scalar
        :param string name: name of the step
        """

        super().__init__(static=False, name=name)

        self._shape = shape
        self._scalar = scalar

        self._post_constructor()

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self._notify_observers("shape")

    @property
    def scalar(self):
        return self._scalar

    @scalar.setter
    def scalar(self, scalar):
        self._scalar = scalar
        self._notify_observers("scalar")
