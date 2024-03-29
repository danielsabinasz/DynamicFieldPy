from dfpy import NoiseInput
from dfpy.activation_function import Sigmoid
from dfpy.shared import get_default_neural_structure
from dfpy.weight_patterns import CustomWeightPattern

from dfpy.steps import Step, Field, Node
from dfpy.connection import SynapticConnection, DirectConnection

import numpy as np
import tensorflow as tf

class NeuralStructure:
    """Base class for a DFT materialized connectivity structure (MCS).
    """

    def __init__(self):
        self._steps = []
        self._connections_into_steps = []
        self._steps_by_name = {}
        self._step_indices_by_name = {}
        self._add_step_observers = []
        self._add_connection_observers = []

    def add_step(self, step):
        """Adds a step to the mcs.

        :param Step step: step to add
        """
        if step in self._steps:
            raise RuntimeError(f"Trying to add step f{step.name} to the neural structure twice.")

        self._step_indices_by_name[step.name] = len(self._steps)
        self._steps.append(step)
        self._connections_into_steps.append([])
        self._steps_by_name[step.name] = step

        self._handle_step_created(step)

    def _handle_step_created(self, step):
        for observer in self._add_step_observers:
            observer(step)

    def _handle_connection_created(self, connection):
        for observer in self._add_connection_observers:
            observer(connection)

    def register_add_step_observer(self, observer):
        self._add_step_observers.append(observer)

    def register_add_connection_observer(self, observer):
        self._add_connection_observers.append(observer)

    def connect(self, input_step, output_step, kernel_weights=None,
                pointwise_weights=None, activation_function=None, contract_dimensions: list=None,
                contraction_weights: list=None,
                expand_dimensions: list=None):
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

        if not isinstance(input_step, Step):
            raise RuntimeError("Invalid argument supplied for input_step: " + str(input_step))
        if not isinstance(output_step, Step):
            raise RuntimeError("Invalid argument supplied for output_step: " + str(output_step))

        if input_step not in self._steps:
            self.add_step(input_step)
        if output_step not in self._steps:
            self.add_step(output_step)

        #if contraction_weights is not None and len(contract_dimensions) == 1\
        #        and (type(contraction_weights) == list and type(contraction_weights[0]) != list\
        #        or type(contraction_weights) == np.ndarray and len(contraction_weights.shape) == 1):
        #    contraction_weights = [contraction_weights]

        if contract_dimensions is None and isinstance(input_step, Field) and isinstance(output_step, Node):
            contract_dimensions = range(len(input_step.dimensions))

        input_step_index = self._steps.index(input_step)

        # and not isinstance(input_step, NoiseInput)
        if (kernel_weights is not None or pointwise_weights is not None)\
                or (isinstance(input_step, Field) or isinstance(input_step, Node))\
                and (isinstance(output_step, Field) or isinstance(output_step, Node)):
            # The user intends a synaptic connection
            if activation_function is None:
                if isinstance(input_step, Field) or isinstance(input_step, Node):
                    activation_function = input_step.activation_function
                else:
                    activation_function = Sigmoid(1)
                    #raise RuntimeError(f"Cannot connect a {type(input_step)} synaptically without providing an "
                    #                   f"activation function")

            if type(kernel_weights) == list or isinstance(kernel_weights, np.ndarray)\
                    or isinstance(kernel_weights, tf.Tensor):
                kernel_weights = CustomWeightPattern(kernel_weights)

            if type(pointwise_weights) == list or isinstance(pointwise_weights, np.ndarray)\
                    or isinstance(pointwise_weights, tf.Tensor):
                pointwise_weights = CustomWeightPattern(pointwise_weights)

            connection = SynapticConnection(input_step, input_step_index, output_step, kernel_weights,
                                            pointwise_weights, activation_function, contract_dimensions,
                                            contraction_weights,
                                            expand_dimensions)
        else:
            connection = DirectConnection(input_step, input_step_index, output_step, kernel_weights,
                                          contract_dimensions,
                                          contraction_weights,
                                          expand_dimensions)

        output_step_index = self._steps.index(output_step)
        self._connections_into_steps[output_step_index].append(connection)

        self._handle_connection_created(connection)

        return connection

    @property
    def steps(self):
        """Returns the steps of the mcs.

        :return: steps of the mcs
        """
        return self._steps

    @property
    def input_steps(self, step):
        """Returns input steps to a given step.

        :param Step step: step
        :return: input steps to the given step
        """
        step_index = self._steps.index(step)
        return self._input_steps_by_step[step_index]

    @property
    def connections_into_steps(self):
        """Returns an array containing the input steps for each step

        :return: array containing the input steps for each step
        """
        return self._connections_into_steps

    def get_step_by_name(self, name: str):
        return self._steps_by_name[name]

    def get_step_index_by_name(self, name: str):
        return self._step_indices_by_name[name]

    def get_connection_by_step_names(self, input_step_name: str, output_step_name: str):
        input_step = self.get_step_by_name(input_step_name)
        output_step = self.get_step_by_name(output_step_name)
        output_step_index = self._steps.index(output_step)
        connections_into_output_step = self._connections_into_steps[output_step_index]
        connection = None
        for conn in connections_into_output_step:
            if conn.input_step == input_step:
                connection = conn
                break
        return connection


def add_step(step):
    ns = get_default_neural_structure()
    return ns.add_step(step)