# Logic lab

Task 0

The initial state is {At(Robot,A), At(Package,A)}. The goal is At(Package,C), so getting only the robot to C is not enough.

The robot can move A to B, B to A, B to C and C to B. A move needs the robot to be at its starting location. It removes the old robot position and adds the new one. It does not change the package's location if the package has not been picked up.

PickUp(Package,X) needs both the robot and package at X. It removes At(Package,X) and adds Holding(Package). The code also checks that the package is not already being held. Drop(Package,X) needs the robot at X and Holding(Package). It removes Holding(Package) and adds At(Package,X).

At the start, PickUp(Package,A) is allowed because both required facts are present. Move(A,B) is also allowed. Drop(Package,C) is not allowed: the robot is not at C and it is not holding the package. An action being available in the model does not mean its preconditions hold right now.

Task 1

The plan is PickUp(Package,A), Move(A,B), Move(B,C), Drop(Package,C).

Initially: At(Robot,A), At(Package,A).
After pickup: At(Robot,A), Holding(Package).
After moving to B: At(Robot,B), Holding(Package).
After moving to C: At(Robot,C), Holding(Package).
After dropping: At(Robot,C), At(Package,C).

This takes four actions. We need to pick up, make two connected moves and drop, so a shorter plan is not possible. Moving to B first and then trying to pick up at B would fail because the package would still be at A.

Tasks 2 and 3

In `planner.py`, a state is a set of facts. `applicable` checks that all positive preconditions are present and all negative preconditions are absent. `apply` removes the delete effects and adds the new facts. BFS uses a queue to explore action sequences, and it stops when all goal facts are in the state. Previously reached states are skipped so that loops do not keep the search running forever.

For the original problem, initial state {At(Robot,A), At(Package,A)} and goal {At(Package,C)}, the four-action plan above was found. Replaying it showed that every action's preconditions held and the final state contained the goal.

With pickup actions removed, the same initial state and goal gave no plan. Moving the robot around cannot deliver the package because there is no action left that can pick it up.

For the irrelevant-movement check, executing Move(A,B), Move(B,C) without pickup leaves {At(Robot,C), At(Package,A)}. The goal is still false. The full planner still finds the four-action delivery plan instead of accepting the robot's arrival as delivery.

Tasks 4 and 5

The missing step in the flow is to apply the action's delete and add effects. Logic checks which actions are legal in a state and calculates the resulting facts. Search then chooses which of those legal alternatives to explore. Both are needed: checking one legal action does not by itself tell us the whole route to the goal.

For the returned plan, pickup is legal at A, the moves start from the robot's actual positions, and drop is legal at C because the robot is still holding the package. The executed state changes agree with this explanation. They are stronger evidence than an explanation alone, although the rules used by the program must also be checked.

Python reflection questions

1. Writing preconditions and effects first gives a clear meaning to each action. It makes it easier to check that the generated code represents the intended problem.

2. Without checking preconditions, the program could drop the package at C while the robot is at A and is not holding anything. This would produce a false solution.

3. A plan can sound reasonable while containing an impossible move or pickup at the wrong place. Each step must be valid in the state produced by the previous step.

4. The LLM helped implement the action representation, BFS queue and path reconstruction. The rules and the results still needed checking against the problem.

5. The checks covered action applicability, state changes, the final package goal and termination when no plan exists. The robot-only movement check also confirmed that robot position and package position are different facts.

6. Logical reasoning happens when checking preconditions and when checking whether the goal follows from the current facts. The action effects describe how those facts change.

7. This is a search problem where states are sets of facts instead of grid positions. Actions connect states, and BFS finds a plan with the fewest actions when every action has the same cost.

Task 6 - Prolog

The Prolog code is in `planner.pl`. From this folder, run `swipl planner.pl`, then enter the queries at the `?-` prompt. Use `halt.` to exit.

`can_move(a,b).` gives true. The fact connected(a,b) is present, and the can_move rule uses that fact.

`can_move(a,c).` gives false. There is a route through B, but there is no direct connected(a,c) fact. The rule checks one direct connection; it does not recursively search for a route.

The rule `can_move(X,Y) :- connected(X,Y).` means that connected(X,Y) implies can_move(X,Y). Prolog tries to establish connected(X,Y) when asked whether can_move(X,Y) holds.

Task 7

`valid_move(a,b).` gives true.
`valid_move(b,c).` gives true.
`valid_move(a,c).` gives false.

So the proposed moves a to b followed by b to c are supported, but a single move a to c is rejected. The direct connection needed for that action is missing.

These rules only check the connections for movement. They do not check pickup, holding or whether a package was delivered. Checking the full delivery plan would also need rules for those facts and state changes.

Task 8

`reduce_speed.` gives true. wet_road is a fact. The first rule derives slippery from wet_road, and the second derives reduce_speed from slippery.

The reasoning is: wet_road => slippery => reduce_speed.

The penguin example is also included: penguin(polly) => bird(polly) => animal(polly), so `animal(polly).` gives true.

Prolog reflection questions

1. A fact states something directly, like connected(a,b). A rule says that a conclusion holds if its conditions can be established, like can_move(X,Y) if connected(X,Y).

2. A query asks Prolog to establish a goal using the facts and rules. For example, can_move(a,b) succeeds because its required connected fact is present. Failure means it could not establish the goal from this program.

3. Python can generate a candidate plan and Prolog can check whether its moves agree with the warehouse connections. This can catch an unsupported direct move such as a to c.

4. A separate verifier gives a check that does not just repeat the generator's explanation. It can catch mistakes in the proposed output, but its own rules must be correct and must cover the property being checked.

Extra task - three rooms and a key

The robot starts in A, the key is in A and the door between B and C is locked. The goal is to reach C. The only connections are A-B and B-C, so there is no direct move from A to C. Moving back along these connections is allowed. The key stays with the robot after unlocking, and the door stays open.

The initial state is {At(Robot,A), At(Key,A), DoorLocked(B,C)}. The goal is {At(Robot,C)}. Each action costs one step.

Actions and their conditions:

- PickUp(Key,A): the robot and key must both be in A, and the robot must not already hold the key. It adds Holding(Key) and removes At(Key,A). It fails if the robot is elsewhere or the key is missing.
- Move(A,B) and Move(B,A): the robot must be in the starting room. A move removes the old robot position and adds the new one. The B-C door does not affect these moves.
- Unlock(B,C): the robot must be in B, hold the key and have a locked door to open. It adds DoorOpen(B,C) and removes DoorLocked(B,C). Without the key or from the wrong room, this action fails.
- Move(B,C) and Move(C,B): the robot must be in the starting room and DoorOpen(B,C) must hold. Crossing while the door is locked is not allowed. The move changes only the robot's position.

Move(A,C) is not an action in this problem because those rooms are not directly connected. The key cannot open a new route; it only opens the existing B-C door.

The plan is PickUp(Key,A), Move(A,B), Unlock(B,C), Move(B,C).

Initially: At(Robot,A), At(Key,A), DoorLocked(B,C).
After pickup: At(Robot,A), Holding(Key), DoorLocked(B,C).
After moving to B: At(Robot,B), Holding(Key), DoorLocked(B,C).
After unlocking: At(Robot,B), Holding(Key), DoorOpen(B,C).
After moving to C: At(Robot,C), Holding(Key), DoorOpen(B,C).

The final state satisfies the goal. Four actions are necessary: one pickup, two moves and one unlock. Going to B without the key does not make the whole problem impossible if returning to A is allowed, but the robot must go back to collect it before it can unlock the door.

`rooms_key.py` uses the same Action representation and BFS from `planner.py`. It prints the plan and state after each step. Run it with `python rooms_key.py` from the logic folder. The original problem gives the four-action plan above. If the key is missing, or the unlock action is removed, it reports no plan. If the B-C connection were removed, unlocking alone would also be insufficient to reach C.

The Prolog version is included in `planner.pl`. A state is written as room_state(Room,KeyStatus,DoorStatus). The key status is on_floor or held, and the door is locked or open. Unlike the earlier simple connection queries, these rules check the key and door state while replaying actions.

`check_room_plan([pick_up_key,move(a,b),unlock,move(b,c)], room_state(a,on_floor,locked), room_state(c,held,open)).` gives true.

Trying `[move(a,b),unlock,move(b,c)]` fails because the robot has no key. Trying `[pick_up_key,move(a,b),move(b,c)]` fails because the door is still locked. Trying `[move(a,c)]` also fails because there is no direct connection.
