"""A small STRIPS-style planner using sets of facts and breadth-first search."""
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    name: str
    positive_preconditions: frozenset
    negative_preconditions: frozenset
    add_effects: frozenset
    delete_effects: frozenset

    def applicable(self, state):
        return self.positive_preconditions <= state and not (self.negative_preconditions & state)

    def apply(self, state):
        if not self.applicable(state):
            raise ValueError('Unsatisfied preconditions: ' + self.name)
        return (state - self.delete_effects) | self.add_effects


def robot(location):
    return f'At(Robot,{location})'


def package(location):
    return f'At(Package,{location})'


HOLDING = 'Holding(Package)'
INITIAL = frozenset([robot('A'), package('A')])
GOAL = frozenset([package('C')])


def warehouse_actions():
    actions = []
    for src, dst in [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B')]:
        actions.append(Action(f'Move({src},{dst})', frozenset([robot(src)]), frozenset(),
                              frozenset([robot(dst)]), frozenset([robot(src)])))
    for location in 'ABC':
        actions.append(Action(f'PickUp(Package,{location})',
                              frozenset([robot(location), package(location)]), frozenset([HOLDING]),
                              frozenset([HOLDING]), frozenset([package(location)])))
        actions.append(Action(f'Drop(Package,{location})', frozenset([robot(location), HOLDING]),
                              frozenset(), frozenset([package(location)]), frozenset([HOLDING])))
    return actions


def plan(initial, goal, actions):
    initial, goal = frozenset(initial), frozenset(goal)
    frontier, parents = deque([initial]), {initial: None}
    while frontier:
        state = frontier.popleft()
        if goal <= state:
            steps, states = [], [state]
            while parents[state] is not None:
                previous, action = parents[state]
                steps.append(action)
                states.append(previous)
                state = previous
            return steps[::-1], states[::-1]
        for action in actions:
            if action.applicable(state):
                nxt = action.apply(state)
                if nxt not in parents:
                    parents[nxt] = (state, action)
                    frontier.append(nxt)
    return None


def verify(initial, goal, steps):
    state = frozenset(initial)
    for action in steps:
        if not action.applicable(state):
            return False
        state = action.apply(state)
        assert sum(robot(x) in state for x in 'ABC') == 1
        assert sum(package(x) in state for x in 'ABC') + (HOLDING in state) == 1
    return frozenset(goal) <= state


if __name__ == '__main__':
    actions = warehouse_actions()
    wait = Action('Wait', frozenset(), frozenset(), frozenset(), frozenset())
    cases = {'Solvable': actions,
             'No pickup': [a for a in actions if not a.name.startswith('PickUp')],
             'Irrelevant action': actions + [wait]}
    for name, available in cases.items():
        print('\n' + name)
        print('Initial:', sorted(INITIAL), 'Goal:', sorted(GOAL))
        solution = plan(INITIAL, GOAL, available)
        if solution is None:
            print('No plan found')
        else:
            steps, states = solution
            assert verify(INITIAL, GOAL, steps)
            print('Initial state:', sorted(states[0]))
            for action, state in zip(steps, states[1:]):
                print(action.name, '->', sorted(state))
