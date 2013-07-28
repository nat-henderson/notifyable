import os

__all__ = [name.split('.')[0] for name in os.listdir(os.path.dirname(__file__))]
