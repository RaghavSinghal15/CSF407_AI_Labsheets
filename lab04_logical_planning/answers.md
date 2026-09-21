# Logical planning

## Task 0

Initial facts: At(Robot,A), At(Package,A). Goal: At(Package,C). Missing facts are treated as false.

Moves are allowed between A and B, and between B and C, in both directions.

- Move(X,Y) needs At(Robot,X). It removes that fact and adds At(Robot,Y).
- PickUp(Package,X) needs robot and package at X, with the package not already held. It removes At(Package,X) and adds Holding(Package).
- Drop(Package,X) needs robot at X and Holding(Package). It removes Holding(Package) and adds At(Package,X).

Initially, moving A to B and picking up at A are allowed. Dropping at C is not allowed because the robot is at A and is not holding the package.

## Task 1: Plan

1. Pick up at A: At(Robot,A), Holding(Package).
2. Move A to B: At(Robot,B), Holding(Package).
3. Move B to C: At(Robot,C), Holding(Package).
4. Drop at C: At(Robot,C), At(Package,C).

This is a shortest plan: pickup, two moves and drop are necessary. Moving to B first leaves the package at A, so pickup at B would fail.

## Tasks 2–3: Code and results

States are immutable sets of facts. `applicable` checks preconditions and `apply` removes delete effects and adds new facts. BFS explores states until the goal facts are present.

The original problem produced the four-action plan above. Removing pickup actions gave no plan. Adding an irrelevant Wait action still gave the same four-action plan.

The code prints and replays each step with precondition checks. Moving the robot alone does not move an unheld package.

## Tasks 4–5

The missing step is to apply the action's delete and add effects after checking its preconditions. Logic decides which actions are allowed and what facts change. Search chooses which states to explore.

Each action in the plan is valid in the preceding state, and the final state has the package at C. Replaying transitions checks the plan more reliably than reading an explanation alone.

## Reflection

1. Preconditions and effects make action behaviour clear and checkable.
2. Without preconditions, the planner could incorrectly drop a package it does not hold.
3. A plausible plan could use disconnected moves or pick up at the wrong location.
4. The LLM helped implement actions and BFS.
5. Preconditions, state changes, final goal and failure termination were checked.
6. Logical reasoning is used in precondition and goal checks.
7. This searches sets of facts instead of grid positions. BFS minimizes the number of actions when their costs are equal.
