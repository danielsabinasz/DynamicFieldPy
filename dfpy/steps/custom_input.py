from dfpy.steps.input import Input
import numpy as np

class CustomInput(Input):
    """Computes a static custom input
    """
    def __init__(self, pattern, dimensions: list = None, name="CustomInput"):
        """Creates a CustomInput.

        :param pattern: the custom input pattern
        :param dimensions: dimensions over which the custom input pattern is defined
        :param string name: name of the step
        """

        super().__init__(static=True, name=name)
        self._pattern = np.array(pattern)
        self._dimensions = dimensions

        self._post_constructor()

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = np.array(pattern)
        self._notify_observers("pattern")

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions
        self._notify_observers("dimensions")

    def dimensionality(self):
        return len(self._pattern.shape)