from enum import Enum
from collections import namedtuple
from itertools import zip_longest

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent     = namedtuple("Agent", ("name", "category"))


def _improve(cat: Condition) -> Condition:
    """One‐step improvement (Dying->Sick, Sick->Healthy)."""
    if cat is Condition.DYING:
        return Condition.SICK
    if cat is Condition.SICK:
        return Condition.HEALTHY
    return cat


def _worsen(cat: Condition) -> Condition:
    """One‐step worsening (Sick->Dying, Dying->Dead)."""
    if cat is Condition.SICK:
        return Condition.DYING
    if cat is Condition.DYING:
        return Condition.DEAD
    return cat


def meetup(agent_listing: tuple) -> list:
    """
    Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """

    # 1) Separate out those who actually meet:
    to_meet = [
        a for a in agent_listing
        if a.category not in (Condition.HEALTHY, Condition.DEAD)
    ]
    # 2) Keep healthy & dead around unchanged:
    untouched = [
        a for a in agent_listing
        if a.category in (Condition.HEALTHY, Condition.DEAD)
    ]

    result = []
    # 3) Pair them off (last one unpaired -> b is None):
    for a, b in zip_longest(*[iter(to_meet)]*2, fillvalue=None):
        if b is None:  # odd one out
            result.append(a)
        else:
            # if one is CURE, it helps the other
            if a.category is Condition.CURE and b.category is not Condition.CURE:
                new_a = a
                new_b = b._replace(category=_improve(b.category))
            elif b.category is Condition.CURE and a.category is not Condition.CURE:
                new_a = a._replace(category=_improve(a.category))
                new_b = b
            # two cures -> nothing changes
            elif a.category is Condition.CURE and b.category is Condition.CURE:
                new_a, new_b = a, b
            # otherwise both worsen
            else:
                new_a = a._replace(category=_worsen(a.category))
                new_b = b._replace(category=_worsen(b.category))

            result.extend([new_a, new_b])

    # 4) Return all agents
    return untouched + result
