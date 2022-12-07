from enum import Enum
from typing import Union

from dfpy.shared import get_default_neural_structure
from dfpy.weight_patterns import WeightPattern
from dfpy.steps import Node, Step
from dfpy.activation_function import ActivationFunction


class Connection():
    def __init__(self, input_step, input_step_index, output_step, name="Connection"):
        self._input_step = input_step
        self._input_step_index = input_step_index
        self._output_step = output_step
        self._name = name

    @property
    def input_step_index(self):
        return self._input_step_index

    @property
    def input_step(self):
        return self._input_step


class DirectConnection(Connection):
    def __init__(self, input_step, input_step_index, output_step, contract_dimensions: list=None,
                 contraction_weights: list=None,
                 expand_dimensions: list=None, name="Direct Connection"):
        super().__init__(input_step, input_step_index, output_step, name)
        self._contract_dimensions = contract_dimensions
        self._contraction_weights = contraction_weights
        self._expand_dimensions = expand_dimensions

    @property
    def contract_dimensions(self):
        return self._contract_dimensions

    @property
    def contraction_weights(self):
        return self._contraction_weights

    @property
    def expand_dimensions(self):
        return self._expand_dimensions


class SynapticConnection(Connection):
    def __init__(self, input_step: Step, input_step_index: int, output_step: Step,
                 kernel_weights: Union[float, int, list, WeightPattern],
                 pointwise_weights: Union[float, int, list, WeightPattern],
                 activation_function: ActivationFunction,
                 contract_dimensions: list=None, contraction_weights: list=None, expand_dimensions: list=None,
                 normalization_type: str="sum",
                 name: str="Synaptic Connection"):
        """Creates a SynapticConnection.

        :param input_step: input step
        :param input_step_index: input step index
        :param output_step: output step
        :param kernel_weights: the synaptic weight pattern of the kernel
        :param pointwise_weights: the pointwise synaptic weight pattern
        :param activation_function: the activation function of the connection
        :param contract_dimensions: dimensions to contract
        :param expand_dimensions: dimensions to expand
        :param contraction_weights: weights for the contraction (if any)
        :param normalization_type: normalization type (as of now, only "sum" is possible)
        :param name: name of the connection
        """
        super().__init__(input_step, input_step_index, output_step, name)

        if type(kernel_weights) == int:
            kernel_weights = float(kernel_weights)
        if type(pointwise_weights) == int:
            pointwise_weights = float(pointwise_weights)
        self._kernel_weights = kernel_weights
        self._pointwise_weights = pointwise_weights
        self._activation_function = activation_function

        self._contract_dimensions = contract_dimensions
        self._contraction_weights = contraction_weights
        self._expand_dimensions = expand_dimensions
        self._normalization_type = normalization_type

    @property
    def kernel_weights(self):
        return self._kernel_weights

    @property
    def pointwise_weights(self):
        return self._pointwise_weights

    @pointwise_weights.setter
    def pointwise_weights(self, pointwise_weights):
        self._pointwise_weights = pointwise_weights

    @property
    def activation_function(self):
        return self._activation_function

    @property
    def contract_dimensions(self):
        return self._contract_dimensions

    @property
    def contraction_weights(self):
        return self._contraction_weights

    @property
    def expand_dimensions(self):
        return self._expand_dimensions


def connect(source, target, kernel_weights=None, pointwise_weights=None, activation_function=None,
            contract_dimensions=[], contraction_weights=None, expand_dimensions=[], ns=None):
    """Connects two steps.

    :param Step input_step: input step of the connection
    :param Step output_step: output step of the connection
    :param kernel_weights: synaptic weight pattern of the kernel
    :param pointwise_weights: pointwise synaptic weight pattern
    :param contract_dimensions: dimensions to contract
    :param contraction_weights: weights for the contraction (if any)
    :param expand_dimensions: dimensions to expand
    :param activation_function: the activation function of the connection
    """
    if ns is None:
        ns = get_default_neural_structure()

    source_dim = source.dimensionality()
    target_dim = target.dimensionality()
    if source_dim > target_dim:
        if source_dim - len(contract_dimensions) != target_dim:
            raise RuntimeError(f"Connecting a step of dimensionality {source_dim} to a step of "
                               f"dimensionality {target_dim} requires {source_dim - target_dim} contractions. "
                               f"Specify a list of contracted dimension indices using the "
                               f"`contract_dimensions` parameter!")

    return ns.connect(source, target, kernel_weights, pointwise_weights, activation_function,
                       contract_dimensions, contraction_weights,
                       expand_dimensions)
