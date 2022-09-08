from mango.core.agent import Agent

from mango_ui.introspection import UIProperty, ui_class


@ui_class
class SuperAgent(Agent):
    def __init__(self, container):
        super().__init__(container)

        self._a = None

    @UIProperty(p_type=int, p_presets=[1, 2, 3])
    def a(self):
        return self._a


@ui_class
class MegaAgent(Agent):
    def __init__(self, container):
        super().__init__(container)

        self._b = None
        self._c = None
        self._d = None
        self._e = None

    @UIProperty(p_type=str, p_presets=[1, 2, 3, 4])
    def b(self):
        return self._b

    @UIProperty(p_type=str, p_presets=[1, 2, 3, 4])
    def c(self):
        return self._c

    @UIProperty(p_type=str, p_presets=[1, 2, 3, 4])
    def d(self):
        return self._d

    @UIProperty(p_type=str, p_presets=[1, 2, 3, 4])
    def e(self):
        return self._e


ALL_AGENTS = [SuperAgent, MegaAgent]
