from typing import Any, Dict
from mango.core.agent import Agent

from mango_ui.introspection import UIProperty, ui_class
from mango.core.container import TCPContainer, MQTTContainer


@ui_class
class SuperAgent(Agent):
    def __init__(self, container):
        super().__init__(container)

        self._a = None

    @UIProperty(p_type=int, p_presets=[1, 2, 3])
    def a(self):
        return self._a

    @a.setter
    def a(self, new_value):
        self._a = new_value


async def print_something(s):
    print(s)


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

    @b.setter
    def b(self, new_value):
        self._b = new_value

    def start(self):
        self._scheduler.schedule_instant_task(print_something(self._b))

    def handle_msg(self, content, meta: Dict[str, Any]):
        pass

    @UIProperty(p_type=str, p_presets=[1, 2, 3, 4])
    def c(self):
        return self._c

    @c.setter
    def c(self, new_value):
        self._c = new_value

    @UIProperty(p_type=str, p_presets=[1, 2, 3, 4])
    def d(self):
        return self._d

    @d.setter
    def d(self, new_value):
        self._d = new_value

    @UIProperty(p_type=str, p_presets=[1, 2, 3, 4])
    def e(self):
        return self._e

    @e.setter
    def e(self, new_value):
        self._e = new_value


ALL_AGENTS = [SuperAgent, MegaAgent]
ALL_CONT = [TCPContainer, MQTTContainer]
