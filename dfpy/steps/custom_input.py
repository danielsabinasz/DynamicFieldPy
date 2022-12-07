from dfpy.steps.input import Input
import numpy as np

class CustomInput(Input):
    """Computes a static custom input
    """
    def __init__(self, pattern, name="CustomInput"):
        """Creates a CustomInput.

        :param array_like pattern: the custom input pattern
        :param string name: name of the step
        """

        super().__init__(static=True, name=name)
        self._pattern = np.array(pattern)

        self._post_constructor()

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = np.array(pattern)
        self._notify_observers("pattern")

    def dimensionality(self):
        return len(self._pattern.shape)