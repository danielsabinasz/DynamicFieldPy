from dfpy.steps.input import Input


class NoiseInput(Input):
    """Computes a normal noise input
    """
    def __init__(self, dimensions: list, strength: float = 1.0, name="NoiseInput"):
        """Creates a NoiseInput.

        :param array_like shape: the shape
        :param strength: the strength of the noise (multiplier)
        :param string name: name of the step
        """

        super().__init__(static=False, name=name)
        self._dimensions = dimensions
        self._shape = tuple([dim.size for dim in dimensions])
        self._strength = strength

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, strength):
        self._strength = strength
