from typing import Union

from dfpy import dimensions_from_sizes
from dfpy.weight_patterns import WeightPattern, RepeatWeightPattern, GaussWeightPattern, SumWeightPattern
from dfpy.activation_function import Sigmoid
from dfpy.activation_function import ActivationFunction
from dfpy.steps.step import Step


class FieldStack(Step):
    """Computes a neural field dynamics.
    """
    def __init__(self, fields, name="FieldStack"):
        """Creates a neural field stack.

        :param fields: list of `Field` objects
        :param string name: name of the step
        """

        super().__init__(name=name)

        self._fields = fields

        self._post_constructor()

    @property
    def fields(self):
        return self._fields


