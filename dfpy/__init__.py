from dfpy.dimension import Dimension, dimensions_from_sizes
from dfpy.steps import *
from dfpy.neural_structure import NeuralStructure
from dfpy.neural_structure import add_step
from dfpy.activation_function import *
from dfpy.weight_patterns import *
from dfpy.connection import connect
import dfpy.utils
import dfpy.shared
import dfpy.config


def initialize_architecture():
    dfpy.shared._default_ns = NeuralStructure()


initialize_architecture()
