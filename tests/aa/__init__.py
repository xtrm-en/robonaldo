from .prop_deleg import context

__all__ = ["context"]

def __getattr__(name):
    if name == 'c':
        return 3
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")