import numpy as np


class PrintToMixin:

    def print_to(self, path):
        with open(path, "wt") as file:
            print(self, file=file)


class StrMixin:

    def __str__(self):
        return "\n".join([str(row) for row in self._data.tolist()])


class PropertiesMixin:

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def shape(self):
        return np.shape(self._data)


class MixinMatrix(np.lib.mixins.NDArrayOperatorsMixin, PropertiesMixin, StrMixin, PrintToMixin):

    def __init__(self, data):
        self._data = data

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """Based on sample in NDArrayOperatorsMixin description"""

        inputs = tuple(x._data if isinstance(x, MixinMatrix) else x for x in inputs)

        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)
