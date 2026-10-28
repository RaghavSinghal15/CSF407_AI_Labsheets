"""Reach room C by collecting the key in A and unlocking the B-C door."""
from planner import Action, plan, robot

KEY = 'At(Key,A)'
HOLDING_KEY = 'Holding(Key)'
LOCKED = 'DoorLocked(B,C)'
OPEN = 'DoorOpen(B,C)'
INITIAL = frozenset([robot('A'), KEY, LOCKED])
GOAL = frozenset([robot('C')])


def room_actions():
    actions = [
        Action('PickUp(Key,A)', frozenset([robot('A'), KEY]),
               frozenset([HOLDING_KEY]), frozenset([HOLDING_KEY]), frozenset([KEY])),
        Action('Unlock(B,C)', frozenset([robot('B'), HOLDING_KEY, LOCKED]),
               frozenset(), frozenset([OPEN]), frozenset([LOCKED]))
    ]
    for src, dst in [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B')]:
        required = {robot(src)}
        if (src, dst) in [('B', 'C'), ('C', 'B')]:
            required.add(OPEN)
        actions.append(Action(f'Move({src},{dst})', frozenset(required), frozenset(),
                              frozenset([robot(dst)]), frozenset([robot(src)])))
    return actions


if __name__ == '__main__':
    actions = room_actions()
    cases = [
        ('Original problem', INITIAL, actions),
        ('Key missing', INITIAL - {KEY}, actions),
        ('Unlock action unavailable', INITIAL,
         [a for a in actions if a.name != 'Unlock(B,C)'])
    ]
    for name, initial, available in cases:
        print('\n' + name)
        print('Initial:', sorted(initial), 'Goal:', sorted(GOAL))
        solution = plan(initial, GOAL, available)
        if solution is None:
            print('No plan found')
        else:
            steps, states = solution
            for action, state in zip(steps, states[1:]):
                print(action.name, '->', sorted(state))
