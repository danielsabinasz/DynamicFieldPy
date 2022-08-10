import inspect

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from dfpy.neural_structure import NeuralStructure
from dfpy.shared import get_default_neural_structure, set_default_neural_structure


class ArchitectureMonitor(PatternMatchingEventHandler):
    def __init__(self, mcs, simulator, filename):
        super().__init__(patterns=[filename])
        self._mcs = mcs
        self._simulator = simulator
        observer = Observer()
        observer.schedule(self, path=filename, recursive=False)
        observer.start()

    def _merge(self, old_object, new_object):
        changed = False
        for prop_name, old_value in inspect.getmembers(old_object):
            if prop_name.startswith("_") or inspect.ismethod(old_value):
                continue
            new_value = getattr(new_object, prop_name)
            if old_value != new_value:
                # TODO see how this has to change
                #if isinstance(new_value, Kernel):
                #    if self._merge(old_value, new_value):
                #        changed = True
                #    continue
                changed = True
                print(old_object, prop_name, new_value)
                setattr(old_object, prop_name, new_value)
        return changed

    def on_modified(self, event):
        filename = event.src_path

        # Store old architecture
        old_mcs = get_default_neural_structure()

        # Create new architecture from file
        new_mcs = NeuralStructure()
        set_default_neural_structure(new_mcs)
        exec(open(filename).read().replace("Ide()", "#Ide()"))

        # Make the old architecture the default architecture
        set_default_neural_structure(old_mcs)

        # Merge the new architecture into the old one
        for old_step in old_mcs.steps:
            new_step = new_mcs.get_step_by_name(old_step.name)
            changed = self._merge(old_step, new_step)

            # If the step changed, recompute tensors for the simulation
            if changed:
                self._simulator.prepare_constants_and_variables_for_step(old_step)
                self._simulator.prepare_time_invariant_tensors_for_step(old_step)
                if old_step.static:
                    self._simulator.reset_step_to_initial_value(old_step)
