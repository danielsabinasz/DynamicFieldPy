class ActivationFunction():
    """Base class for activation functions (e.g., sigmoid)
    """


class Sigmoid(ActivationFunction):
    """Computes the sigmoid of its input.
    """
    def __init__(self, beta: float=100.0):
        """Creates a sigmoid.

        :param float beta: steepness parameter of the sigmoid
        :param string name: name of the step
        """

        super().__init__()

        if type(beta) == int:
            beta = float(beta)

        self._beta = beta

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, beta):
        self._beta = beta

    def __str__(self):
        return "Sigmoid(beta=" + str(self._beta) + ")"


class Identity(ActivationFunction):
    pass
