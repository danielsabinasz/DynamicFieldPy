from dfpy import dimensions_from_sizes
from dfpy.steps.input import Input
import numpy as np

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

        if type(dimensions) == tuple:
            dimensions = dimensions_from_sizes(*dimensions)

        self._dimensions = dimensions
        self._height = height

        ndim = len(self._dimensions)

        # Mean is zero by default
        if mean is None:
            mean = [0.0]*ndim
        if type(mean) == float or type(mean) == int:
            mean = [float(mean)]
        if type(mean) == np.ndarray:
            if mean.dtype != np.float32:
                raise RuntimeError("The datatype of the mean must be np.float32")

        self._mean = mean

        # Stddev is 1 in each dimension by default
        if sigmas is None:
            sigmas = [1.0]*ndim
        if type(sigmas) == float or type(sigmas) == int:
            sigmas = [float(sigmas)]
        self._sigmas = sigmas

        self._post_constructor()

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self._notify_observers("height")

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, mean):
        if type(mean) == float or type(mean) == int:
            mean = [float(mean)]
        self._mean = mean
        self._notify_observers("mean")

    @property
    def sigmas(self):
        return self._sigmas

    @sigmas.setter
    def sigmas(self, sigmas):
        self._sigmas = sigmas
        self._notify_observers("sigmas")

    def domain(self):
        return [[dimension.lower, dimension.upper] for dimension in self._dimensions]

    def shape(self):
        return tuple([dimension.size for dimension in self._dimensions])


    def dimensionality(self):
        return len(self._dimensions)
