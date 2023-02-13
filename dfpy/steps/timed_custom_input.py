from dfpy import dimensions_from_sizes
from dfpy.steps.input import Input


class TimedCustomInput(Input):
    """Computes a timed custom input
    """
    def __init__(self, dimensions: list, timed_custom_input = None, name="TimedCustomInput"):
        """Creates a CustomInput.

        :param dimensions: list of `:class:`.Dimension` objects characterizing the dimensions of the custom input.
        :param array_like timed_custom_input: list of custom input pattern for each time step
        :param string name: name of the step
        """

        super().__init__(name=name)

        if type(dimensions) == tuple:
            dimensions = dimensions_from_sizes(*dimensions)
        elif type(dimensions) != list:
            raise TypeError(f"Dimensions parameter has unsupported type '{type(dimensions)}'. "
                            f"The type must be either a tuple of integers or a list of 'Dimension' objects")

        self._dimensions = dimensions
        self._timed_custom_input = timed_custom_input

        self._post_constructor()

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions
        self._notify_observers("dimensions")

    @property
    def timed_custom_input(self):
        return self._timed_custom_input

    @timed_custom_input.setter
    def timed_custom_input(self, timed_custom_input):
        self._timed_custom_input = timed_custom_input
        self._notify_observers("timed_custom_input")

    def dimensionality(self):
        return len(self._dimensions)