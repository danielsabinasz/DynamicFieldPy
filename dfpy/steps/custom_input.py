from dfpy.steps.input import Input


class CustomInput(Input):
    """Computes a static Gauss input
    """
    def __init__(self, pattern, name="CustomInput"):
        """Creates a CustomInput.

        :param array_like pattern: the custom input pattern
        :param string name: name of the step
        """

        super().__init__(static=True, name=name)
        self._pattern = pattern

        self._post_constructor()

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = pattern
        self._notify_observers()
