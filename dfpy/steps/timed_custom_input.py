from dfpy import dimensions_from_sizes, shape_from_list_of_dimensions
from dfpy.steps.input import Input
import numpy as np

class TimedCustomInput(Input):
    """Computes a timed custom input
    """
    def __init__(self, dimensions: list = None, timed_custom_input = None, num_time_steps = None, name="TimedCustomInput"):
        """Creates a CustomInput.

        :param dimensions: list of `:class:`.Dimension` objects characterizing the dimensions of the custom input.
        :param array_like timed_custom_input: list of custom input pattern for each time step
        :param int num_time_steps: list of custom input pattern for each time step
        :param string name: name of the step
        """

        super().__init__(name=name)

        if type(dimensions) == tuple:
            dimensions = dimensions_from_sizes(*dimensions)
        elif dimensions is not None and type(dimensions) != list:
            raise TypeError(f"Dimensions parameter has unsupported type '{type(dimensions)}'. "
                            f"The type must be either a tuple of integers or a list of 'Dimension' objects")

        if timed_custom_input is None:
            assert num_time_steps is not None, "When no timed_custom_input is provided to the constructor, num_time_steps needs to be specified"
            timed_custom_input = np.zeros(shape=[num_time_steps] + shape_from_list_of_dimensions(dimensions))

        if dimensions is None:
            if type(timed_custom_input[0]) == float:
                dimensions = []
            else:
                raise RuntimeError(f"Dimensions parameter cannot be None")

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