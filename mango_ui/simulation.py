import asyncio

import concurrent.futures

from mango.core.container import Container
from mango.role.core import Agent

import mango_ui.example_agents


def _create_asyncio_context():
    asyncio.set_event_loop(asyncio.new_event_loop())


PROCESS_POOL_EXEC = concurrent.futures.ProcessPoolExecutor(
    max_workers=10, initializer=_create_asyncio_context
)


def _run_task_in_p_context(run_method, data_container, data_agents):
    return asyncio.get_event_loop().run_until_complete(
        run_method(data_container, data_agents)
    )


def exec(run_method, data_container, data_agents):
    return PROCESS_POOL_EXEC.submit(
        _run_task_in_p_context, run_method, data_container, data_agents
    )


async def run_mango_simulation(data_entries_container, data_entries_agent):
    c = None
    for container_entry in data_entries_container:
        container_cls = container_entry[0]
        container_param = container_entry[1]

        c = await Container.factory(addr=("127.0.0.2", 5555))

    print("IM HERE")

    agents = []
    for agent_entry in data_entries_agent:
        agent_entry_cls_str = agent_entry[0]
        agent_param = agent_entry[1]
        agent_obj = None
        for agent in mango_ui.example_agents.ALL_AGENTS:
            if str(agent) == agent_entry_cls_str:
                agent_obj = agent(c)
                agents.append(agent_obj)
        for key, value in agent_param.items():
            setattr(agent_obj, key, value)
        agent_obj.start()

    await asyncio.sleep(10000)


def execute_simulation_with_ui_data(data_entries_container, data_entries_agent):
    return exec(run_mango_simulation, data_entries_container, data_entries_agent)
