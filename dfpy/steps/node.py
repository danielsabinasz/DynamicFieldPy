from dfpy.steps.step import Step
from dfpy.activation_function import Sigmoid


class Node(Step):
    """Computes a neural node dynamics.
    """
    def __init__(self, resting_level=-5.0, time_scale=100, self_excitation=0.0,
                 activation_function=Sigmoid(100.0),
                 noise_strength=0.2,
                 name="Neural Node"):
        """Creates a neural node.

        :param float resting_level: resting level of the field
        :param int time_scale: time scale of the field (parameter tau in the field dynamics)
        :param float sigmoid_beta: beta parameter of the sigmoid (slope)
        :param float self_excitation: self-excitation of the neural node
        :param float noise_strength: amplitude of Gauss white noise
        :param string name: name of the step
        """

        super().__init__(name=name)

        self._resting_level = float(resting_level)
        self._time_scale = float(time_scale)
        self._self_excitation = float(self_excitation)
        self._activation_function = activation_function
        self._noise_strength = float(noise_strength)

    @property
    def resting_level(self):
        return self._resting_level

    @resting_level.setter
    def resting_level(self, resting_level):
        self._resting_level = resting_level

    @property
    def time_scale(self):
        return self._time_scale

    @time_scale.setter
    def time_scale(self, time_scale):
        self._time_scale = time_scale

    @property
    def activation_function(self):
        return self._activation_function

    @activation_function.setter
    def activation_function(self, activation_function):
        self._activation_function = activation_function

    @property
    def self_excitation(self):
        return self._self_excitation

    @self_excitation.setter
    def self_excitation(self, self_excitation):
        self._self_excitation = self_excitation

    @property
    def noise_strength(self):
        return self._noise_strength

    @noise_strength.setter
    def noise_strength(self, noise_strength):
        self._noise_strength = noise_strength
