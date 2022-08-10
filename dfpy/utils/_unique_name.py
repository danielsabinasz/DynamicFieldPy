counters_by_neural_structure = {}


def unique_name(name: str, neural_structure) -> str:
    """
    Turns the passed name into a unique name for a given mcs by adding a unique number to it, if necessary

    :param name: the (possibly non-unique) name that should be turned into a unique name
    :param NeuralStructure neural_structure
    :return: the unique name
    """
    if neural_structure not in counters_by_neural_structure:
        counters_by_neural_structure[neural_structure] = {}
    counters = counters_by_neural_structure[neural_structure]
    if name not in counters:
        counters[name] = 1
        return name
    counters[name] = counters[name] + 1
    return name + " " + str(counters[name])
