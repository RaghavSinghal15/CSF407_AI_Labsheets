# Logic lab

Task 0

Initial state: {At(Robot,A), At(Package,A)}. Goal: At(Package,C). The robot reaching C alone does not deliver the package.

Actions:

- Move(X,Y): needs the robot at X and a connection to Y. Removes At(Robot,X), adds At(Robot,Y). Connections are A-B and B-C in both directions.
- PickUp(Package,X): needs robot and package at X, with the package not already held. Removes At(Package,X), adds Holding(Package).
- Drop(Package,X): needs robot at X and Holding(Package). Removes Holding(Package), adds At(Package,X).

Initially pickup at A and moving A to B are allowed. Drop at C fails because the robot is not there and holds nothing.

Task 1

Plan: PickUp(Package,A) -> Move(A,B) -> Move(B,C) -> Drop(Package,C).

After pickup: robot at A, holding package.
After first move: robot at B, holding package.
After second move: robot at C, holding package.
After drop: robot and package at C.

Four actions are needed: pickup, two moves and drop. Moving to B before pickup leaves the package at A, so pickup at B would fail.

Tasks 2 and 3

`planner.py` stores states as sets of facts. `applicable` checks required and forbidden facts. `apply` removes delete effects and adds new facts. BFS explores states using a queue and skips states already reached.

For initial state {At(Robot,A), At(Package,A)} and goal At(Package,C):

- Original problem: found the four-action plan above. All steps were valid.
- Pickup removed: no plan found.
- Moving A-B-C without pickup: robot reached C, but package stayed at A. Goal was false.

Tasks 4 and 5

The missing step is applying the action's delete and add effects. Logic checks which actions are possible; search explores their possible sequences.

The returned plan's preconditions hold at every step. Executed state changes are better evidence than an explanation alone, provided the encoded rules are correct.

Reflection

1. Preconditions and effects specify what each action actually means, making the generated code easier to check.
2. Without precondition checks, the robot could incorrectly drop a package it never picked up.
3. A reasonable-looking plan can still contain an impossible move or pickup at the wrong place.
4. The LLM helped implement the action representation and BFS.
5. Action validity, state changes, the final goal and no-plan termination were checked.
6. Logic is used in precondition and goal checks.
7. Planning searches sets of facts instead of grid positions. BFS minimizes action count when costs are equal.

Tasks 6 and 7 - Prolog

Run `swipl planner.pl` from this folder. Enter queries at the prompt and use `halt.` to exit.

`can_move(a,b).` is true; `can_move(a,c).` is false.
`valid_move(a,b).` and `valid_move(b,c).` are true; `valid_move(a,c).` is false.

The rules use direct connected facts. A-B and B-C exist, but A-C does not. Having a route through B does not make A-C a single valid move. The rule `can_move(X,Y) :- connected(X,Y).` expresses Connected(X,Y) implies CanMove(X,Y).

These checks verify movement connections, not package delivery.

Task 8

`reduce_speed.` is true: wet_road is a fact, which implies slippery, which implies reduce_speed.

The other example also succeeds: penguin(polly) implies bird(polly), which implies animal(polly).

Prolog reflection

1. A fact states something directly. A rule derives a conclusion when its conditions hold.
2. A query asks whether a goal can be established using the facts and rules.
3. Prolog can independently reject unsupported moves proposed by Python, such as A-C.
4. An independent check can catch generator mistakes, but the verifier's rules must also be correct and cover the property being checked.

Extra task - rooms and key

Initially robot and key are in A, with the B-C door locked. Goal: robot at C. Only A-B and B-C are connected, in both directions. The key is kept after use and the door stays open.

- PickUp(Key,A): needs robot and key in A, without already holding it. Replaces At(Key,A) with Holding(Key).
- Move(X,Y): needs robot at X and a direct connection. Crossing B-C also needs DoorOpen(B,C). Updates the robot's position.
- Unlock(B,C): needs robot at B, Holding(Key) and DoorLocked(B,C). Replaces the locked fact with DoorOpen(B,C).

Plan: pick up key -> A to B -> unlock -> B to C. After pickup the robot holds the key; at B it unlocks the door, then reaches C. This takes four actions.

Without the key, unlock fails. While locked, crossing B-C fails. Direct A-C is never allowed. Going to B without pickup is recoverable by returning to A.

Run `python rooms_key.py`. BFS found this plan; missing key or removing unlock gave no plan. In `planner.pl`, the full room plan passed. Skipping pickup, skipping unlock and direct A-C plans failed.
