import inspect

# @ui_class -> add dictionary, add method for adding to dict
#   name<string>, type, presets (list<type>)
#
# @ui_property -> do some stuff, grab property


def ui_class(cls=None):
    def wrap(cls):
        @classmethod
        def __add_ui_parameter__(self, p_name, p_type, p_presets):
            self.__ui_parameters__[p_name] = (p_type, p_presets)

        cls.__add_ui_parameter__ = __add_ui_parameter__
        cls.__ui_parameters__ = {}

        for x in inspect.getmembers(cls):
            # check for _UIProperty objects
            # extract the param, type, preset info
            # save it in the class!
            obj = getattr(cls, x[0])

            if isinstance(obj, _UIProperty):
                cls.__add_ui_parameter__(obj.p_name, obj.p_type, obj.p_presets)

        return cls

    if cls is None:
        return wrap
    else:
        return wrap(cls)


class _UIProperty(property):
    def __init__(
        self,
        fget=None,
        fset=None,
        fdel=None,
        doc=None,
        p_type=None,
        p_presets=None,
    ):
        self.p_name = fget.__qualname__.split(".")[-1]
        self.p_type = p_type
        self.p_presets = p_presets

        super().__init__(fget, fset, fdel, doc)

    def getter(self, fget):
        return type(self)(
            fget, self.fset, self.fdel, self.__doc__, self.p_type, self.p_presets
        )

    def setter(self, fset):
        return type(self)(
            self.fget, fset, self.fdel, self.__doc__, self.p_type, self.p_presets
        )

    def deleter(self, fdel):
        return type(self)(
            self.fget, self.fset, fdel, self.__doc__, self.p_type, self.p_presets
        )


def UIProperty(function=None, p_type=None, p_presets=None):
    if function:
        return _UIProperty(function, None, None, None, p_type, p_presets)
    else:

        def wrapper(function):
            return _UIProperty(function, None, None, None, p_type, p_presets)

        return wrapper
