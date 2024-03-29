from typing import Union

from dfpy import dimensions_from_sizes
from dfpy.weight_patterns import WeightPattern, RepeatWeightPattern, GaussWeightPattern, SumWeightPattern
from dfpy.activation_function import Sigmoid
from dfpy.activation_function import ActivationFunction
from dfpy.steps.step import Step


class Field(Step):
    """Computes a neural field dynamics.
    """
    def __init__(self, dimensions: list, resting_level: float=-5.0,
                 activation_function: ActivationFunction = Sigmoid(beta=1.0),
                 time_scale: float = 100.0,
                 interaction_kernel: WeightPattern=None, global_inhibition: float=0.0,
                 noise_strength: float=0.1, template = None,
                 name="Field"):
        """Creates a neural field.

        :param dimensions: list of `:class:`.Dimension` objects characterizing the dimensions of the field.
        :param resting_level: resting level of the field
        :param time_scale: time scale of the field (parameter tau in the field dynamics)
        :param sigmoid_beta: beta parameter of the sigmoid (slope)
        :param interaction_kernel: lateral interaction kernel
        :param global_inhibition: global inhibition inside the field
        :param noise_strength: amplitude of Gauss white noise
        :param template: A different field from which to copy parameter values
        :param string name: name of the step
        """

        super().__init__(name=name)

        if type(dimensions) == tuple:
            dimensions = dimensions_from_sizes(*dimensions)
        elif type(dimensions) != list:
            raise TypeError(f"Dimensions parameter has unsupported type '{type(dimensions)}'. The type must be either a tuple of integers or a list of 'Dimension' objects")

        ndim = len(dimensions)

        self._dimensions = dimensions
        self._resting_level = float(resting_level)
        self._activation_function = activation_function
        self._time_scale = float(time_scale)

        if type(interaction_kernel) == str:
            if interaction_kernel == "stabilized":
                interaction_kernel = build_stabilized_kernel(dimensions)
            else:
                raise RuntimeError(f"Unrecognized interaction kernel type '{interaction_kernel}'")

        self._interaction_kernel = interaction_kernel
        self._global_inhibition = float(global_inhibition)
        self._noise_strength = float(noise_strength)

        if self._interaction_kernel is not None and self._interaction_kernel.dimensionality() != len(self._dimensions):
            # If the dimensionality of the interaction kernel is one smaller than the
            # dimensionality of the field, copy the interaction kernel along the
            # additional axis
            if self._interaction_kernel.dimensionality() == len(self._dimensions)-1:
                self._interaction_kernel = RepeatWeightPattern(interaction_kernel, self._dimensions[-1].size)
            else:
                raise RuntimeError(f"Dimensionality of {self._name} does not match the dimensionality of its interaction kernel")

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

    @classmethod
    def from_other(cls, other):
        return Field(
            dimensions=other.dimensions,
            resting_level=other.resting_level,
            activation_function=other.activation_function,
            time_scale=other.time_scale,
            interaction_kernel=other.interaction_kernel,
            global_inhibition=other.global_inhibition,
            noise_strength=other.noise_strength
        )

    def domain(self):
        return [[dimension.lower, dimension.upper] for dimension in self._dimensions]

    def shape(self):
        return tuple([dimension.size for dimension in self._dimensions])

    def dimensionality(self):
        return len(self._dimensions)



def build_stabilized_kernel(dimensions):
    if len(dimensions) == 3:
        return SumWeightPattern([
            GaussWeightPattern(height=0.4, sigmas=(2.0, 2.0, 0.1)),
            GaussWeightPattern(height=-0.11, sigmas=(4.0, 4.0, 0.1))
        ])
    else:
        raise RuntimeError(f"Unsupported dimensionality for stabilized kernel: {len(dimensions)}")
