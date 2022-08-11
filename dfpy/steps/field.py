from typing import Union

from dfpy import dimensions_from_sizes
from dfpy.weight_patterns import WeightPattern
from dfpy.activation_function import Sigmoid
from dfpy.activation_function import ActivationFunction
from dfpy.steps.step import Step


class Field(Step):
    """Computes a neural field dynamics.
    """
    def __init__(self, dimensions: list, resting_level: float=-5.0,
                 activation_function: ActivationFunction = Sigmoid(beta=100),
                 time_scale: float = 100.0,
                 interaction_kernel: WeightPattern=None, global_inhibition: float=0.0,
                 noise_strength: float=0.1,
                 name="Field"):
        """Creates a neural field.

        :param dimensions: list of `:class:`.Dimension` objects characterizing the dimensions of the field.
        :param resting_level: resting level of the field
        :param time_scale: time scale of the field (parameter tau in the field dynamics)
        :param sigmoid_beta: beta parameter of the sigmoid (slope)
        :param interaction_kernel: lateral interaction kernel
        :param global_inhibition: global inhibition inside the field
        :param noise_strength: amplitude of Gauss white noise
        :param string name: name of the step
        """

        super().__init__(name=name)

        if type(dimensions) == tuple:
            dimensions = dimensions_from_sizes(*dimensions)

        self._dimensions = dimensions
        self._resting_level = float(resting_level)
        self._activation_function = activation_function
        self._time_scale = float(time_scale)
        self._interaction_kernel = interaction_kernel
        self._global_inhibition = float(global_inhibition)
        self._noise_strength = float(noise_strength)

        self._post_constructor()

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions
        self._notify_observers("dimensions")

    @property
    def activation_function(self):
        return self._activation_function

    @activation_function.setter
    def activation_function(self, activation_function):
        self._activation_function = activation_function
        self._notify_observers("activation_function")

    @property
    def resting_level(self):
        return self._resting_level

    @resting_level.setter
    def resting_level(self, resting_level):
        self._resting_level = resting_level
        self._notify_observers("resting_level")

    @property
    def time_scale(self):
        return self._time_scale

    @time_scale.setter
    def time_scale(self, time_scale):
        self._time_scale = time_scale
        self._notify_observers("time_scale")

    @property
    def interaction_kernel(self):
        return self._interaction_kernel

    @interaction_kernel.setter
    def interaction_kernel(self, interaction_kernel):
        self._interaction_kernel = interaction_kernel
        self._notify_observers("interaction_kernel")

    @property
    def global_inhibition(self):
        return self._global_inhibition

    @global_inhibition.setter
    def global_inhibition(self, global_inhibition):
        self._global_inhibition = global_inhibition
        self._notify_observers("global_inhibition")

    @property
    def noise_strength(self):
        return self._noise_strength

    @noise_strength.setter
    def noise_strength(self, noise_strength):
        self._noise_strength = noise_strength
        self._notify_observers("noise_strength")

    def domain(self):
        return [[dimension.lower, dimension.upper] for dimension in self._dimensions]

    def shape(self):
        return tuple([dimension.size for dimension in self._dimensions])
