from dfpy.dimension import Dimension, dimensions_from_sizes, shape_from_list_of_dimensions
from dfpy.steps import *
from dfpy.neural_structure import NeuralStructure
from dfpy.neural_structure import add_step
from dfpy.activation_function import *
from dfpy.weight_patterns import *
from dfpy.connection import connect
from dfpy.shared import get_default_neural_structure
import dfpy.utils
import dfpy.shared
import dfpy.config


def initialize_architecture():
    dfpy.shared._default_ns = NeuralStructure()


initialize_architecture()
