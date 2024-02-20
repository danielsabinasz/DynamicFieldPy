from dfpy.utils import unique_name
import dfpy.shared


class Step:
    """Base class for a step.

    :param bool static: whether the step yields the same value on each time step
    :param bool stateful: whether the step is stateful, i.e., the state at a given time-step is relevant for
    computing the state at the next time step
    """
    def __init__(self, neural_structure=None, static=False, stateful=True, inputs=[],
                 name="step"):
        if neural_structure is None:
            neural_structure = dfpy.shared.get_default_neural_structure()

        self._neural_structure = neural_structure
        self._static = static
        self._stateful = stateful
        self._inputs = inputs
        self._name = unique_name(name, neural_structure)
        self._observers = []
        self._trainable = False
        self._assignable = False

    def _post_constructor(self):
        self._neural_structure.add_step(self)

    @property
    def static(self):
        return self._static

    @property
    def stateful(self):
        return self._stateful

    @property
    def inputs(self):
        return self._inputs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        for observer in self._observers:
            observer()

    @property
    def trainable(self):
        return self._trainable

    @trainable.setter
    def trainable(self, trainable):
        self._trainable = trainable
        if trainable:
            self.assignable = True

    @property
    def assignable(self):
        return self._assignable

    @assignable.setter
    def assignable(self, assignable):
        self._assignable = assignable

    def register_observer(self, observer):
        self._observers.append(observer)

    def _notify_observers(self, changed_param):
        for observer in self._observers:
            observer(self, changed_param)
