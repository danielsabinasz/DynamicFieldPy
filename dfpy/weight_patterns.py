import numpy as np

class WeightPattern:
    """Base class for a weight pattern
    """
    pass


class CustomWeightPattern(WeightPattern):
    """A custom weight pattern
    """
    def __init__(self, pattern: list):
        """Creates a CustomWeightPattern

        :param pattern: the pattern
        """
        self._pattern = pattern

    def dimensionality(self):
        return len(np.array(self._pattern).shape)

    @property
    def pattern(self):
        return self._pattern

    def __str__(self):
        return "CustomWeightPattern(pattern=" + ','.join([str(x) for x in self._pattern]) + ")"


class SumWeightPattern(WeightPattern):
    """A sum weight pattern that is the sum of multiple other weight pattern
    """
    def __init__(self, weight_patterns: list, cutoff_factor=4., field_size = None):
        """Creates a SumWeightPattern

        :param weight_patterns: the weight patters to sum
        """
        #cutoff_factor=None
        self._weight_patterns = weight_patterns

        ndim = weight_patterns[0].dimensionality()
        for weight_pattern in weight_patterns:
            if weight_pattern.dimensionality() != ndim:
                raise RuntimeError("Components of SumWeightPattern have non-matching dimensionalities " + str(ndim) + " vs. " + str(weight_pattern.dimensionality()))

        if field_size is not None and cutoff_factor is not None and type(weight_patterns[0]) == GaussWeightPattern and type(weight_patterns[1]) == GaussWeightPattern:
            self._range = computeKernelRange(max(weight_patterns[0].sigmas[0], weight_patterns[1].sigmas[0]), cutoff_factor, field_size, False)
        else:
            self._range = None

    @property
    def weight_patterns(self):
        return self._weight_patterns

    def dimensionality(self):
        return self._weight_patterns[0].dimensionality()

    def range(self):
        return self._range

    def __str__(self):
        return "SumWeightPattern(weight_patterns=" + ','.join([str(x) for x in self._weight_patterns]) + ")"



class RepeatWeightPattern(WeightPattern):
    """A weight pattern that repeats the given weight pattern n times
    """
    def __init__(self, weight_pattern, num_repeats: int):
        """Creates a SumWeightPattern

        :param weight_patterns: the weight patters to repeat
        :param num_repeats: number of repetitions of the weight pattern
        """
        self._weight_pattern = weight_pattern
        self._num_repeats = num_repeats

    @property
    def weight_pattern(self):
        return self._weight_pattern

    @property
    def num_repeats(self):
        return self._num_repeats

    def dimensionality(self):
        return self._weight_pattern.dimensionality()+1

    def __str__(self):
        return "RepeatWeightPattern(weight_pattern=" + str(self._weight_pattern) + ")"



class GaussWeightPattern(WeightPattern):
    """Base class for a Gauss weight pattern
    """
    def __init__(self, height, sigmas, mean=None, cutoff_factor=4., field_size=None):
        """Creates a WeightPatternGauss.
        :param float height: amplitude of the Gauss
        :param array_like mean: mean of the Gauss
        :param array_like sigmas: standard deviation of the Gauss
        """

        if type(sigmas) == int or type(sigmas) == float:
            sigmas = [sigmas]

        self._height = float(height)

        ndim = len(sigmas)

        # Mean is zero by default
        if mean is None:
            mean = [0.0]*ndim
        if type(mean) == float or type(mean) == int:
            mean = [float(mean)]
        self._mean = mean

        # Stddev is 1 in each dimension by default
        if sigmas is None:
            sigmas = [1.0] * ndim
        if type(sigmas) == float or type(sigmas) == int:
            sigmas = [float(sigmas)]
        self._sigmas = sigmas

        if field_size is not None and cutoff_factor is not None:
            self._range = computeKernelRange(sigmas[0], cutoff_factor, field_size, False)
        else:
            self._range = None

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, mean):
        self._mean = mean

    @property
    def sigmas(self):
        return self._sigmas

    @sigmas.setter
    def sigmas(self, sigmas):
        self._sigmas = sigmas

    def dimensionality(self):
        return len(self._sigmas)

    def range(self):
        return self._range

    def __str__(self):
        return "GaussWeightPattern(height=" + str(self._height) + ", mean=" + str(self._mean)\
               + ", sigmas=[" + ','.join([str(x) for x in self._sigmas]) + "])"


class RepeatedValueWeightPattern(WeightPattern):
    """Base class for a weight pattern with repeated values
    """
    def __init__(self, value: float, shape: tuple):
        """Creates a WeightPatternRepeatedValue.
        :param value: the value in each entry
        :param shape
        """
        self._value = value
        self._shape = shape

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    def dimensionality(self):
        return len(self._shape)

    def __str__(self):
        return "RepeatedValueWeightPattern(value=" + str(self._value) + ", shape=" + str(self._shape) + ")"


# By Sebastian Schneegans (https://github.com/cosivina/cosivina_python)
def computeKernelRange(sigma, cutoffFactor, fieldSize, circular = True):
    if circular:
        r = np.ceil(sigma * cutoffFactor)
        h = (fieldSize-1)/2
        return np.array([min(r, np.floor(h)), min(r, np.ceil(h))], dtype=np.int32)
    else:
        r = int(min(np.ceil(sigma * cutoffFactor), (fieldSize - 1)))
        return np.array([r, r], dtype=np.int32)
