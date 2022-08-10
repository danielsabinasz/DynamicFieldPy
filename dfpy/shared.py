# Holds the default materialized neural structure. Not that this structure is created in __init__.py
_default_ns = None


def get_default_neural_structure():
    """Returns the default mcs

    :return MaterializedConnectivityStructure: the default mcs
    """
    global _default_ns
    return _default_ns


def set_default_neural_structure(ns):
    """Sets the default neural structure

    :param mcs: the default neural structure
    """
    global _default_ns
    _default_ns = ns

