from dfpy.steps.step import Step


class RateMatrixToSpaceCode(Step):
    """Computes a 3D tensor T such that T(i,j,k) = values(i, j) if bin_map(i, j) is in the k-th bin,
    where the boundaries of the k-th bin are defined by splitting the range between the specified lower limit and the
    upper limit into the specified number of bins.
    """
    def __init__(self, number_of_bins=10, lower_limit=0.0, upper_limit=1.0, name="Rate Matrix to Space Code"):
        """Creates an Image.

        :param int number_of_bins: number of bins
        :param float lower_limit: lower limit of the values in the map
        :param float upper_limit: upper limit of the values in the map
        :param string name: name of the step
        """

        super().__init__(static=False, stateful=False, inputs=["map", "value"], name=name)

        self._number_of_bins = number_of_bins
        self._lower_limit = lower_limit
        self._upper_limit = upper_limit

    @property
    def number_of_bins(self):
        return self._number_of_bins

    @number_of_bins.setter
    def number_of_bins(self, number_of_bins):
        self._number_of_bins = number_of_bins

    @property
    def lower_limit(self):
        return self._lower_limit

    @lower_limit.setter
    def lower_limit(self, lower_limit):
        self._lower_limit = lower_limit

    @property
    def upper_limit(self):
        return self._upper_limit

    @upper_limit.setter
    def upper_limit(self, upper_limit):
        self._upper_limit = upper_limit
