from dfpy.steps.input import Input


class GaussInput(Input):
    """Computes a static Gauss input
    """
    def __init__(self, dimensions: list, height=1.0, mean=None, sigmas=None, name="GaussInput"):
        """Creates a GaussInput.

        :param float height: height of the Gauss
        :param array_like mean: mean of the Gauss
        :param array_like sigmas: standard deviation of the Gauss
        :param string name: name of the step
        """

        super().__init__(static=True, name=name)
        self._dimensions = dimensions
        self._height = height

        ndim = len(self._dimensions)

        # Mean is zero by default
        if mean is None:
            mean = [0.0]*ndim
        if type(mean) == float or type(mean) == int:
            mean = [float(mean)]
        self._mean = mean

        # Stddev is 1 in each dimension by default
        if sigmas is None:
            sigmas = [1.0]*ndim
        if type(sigmas) == float or type(sigmas) == int:
            sigmas = [float(sigmas)]
        self._sigmas = sigmas

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, mean):
        self._mean = mean

    @property
    def sigmas(self):
        return self._sigmas

    @sigmas.setter
    def sigmas(self, sigmas):
        self._sigmas = sigmas

    def domain(self):
        return [[dimension.lower, dimension.upper] for dimension in self._dimensions]

    def shape(self):
        return tuple([dimension.size for dimension in self._dimensions])