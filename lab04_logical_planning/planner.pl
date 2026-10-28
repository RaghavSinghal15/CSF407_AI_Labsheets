% Warehouse connections and the simple rules from the lab sheet.
connected(a,b).
connected(b,a).
connected(b,c).
connected(c,b).

can_move(X,Y) :-
    connected(X,Y).

valid_move(X,Y) :-
    connected(X,Y).

% Task 8: infer the response from the road condition.
wet_road.

slippery :-
    wet_road.

reduce_speed :-
    slippery.

% Introductory example from the sheet.
penguin(polly).

bird(X) :-
    penguin(X).

animal(X) :-
    bird(X).

% Extra task: the door between B and C needs the key from A.
room_passage(a,b,_).
room_passage(b,a,_).
room_passage(b,c,open).
room_passage(c,b,open).

% room_state(CurrentRoom, KeyStatus, DoorStatus)
room_step(pick_up_key, room_state(a,on_floor,Door), room_state(a,held,Door)).
room_step(unlock, room_state(b,held,locked), room_state(b,held,open)).
room_step(move(X,Y), room_state(X,Key,Door), room_state(Y,Key,Door)) :-
    room_passage(X,Y,Door).

check_room_plan([], State, State).
check_room_plan([Action|Rest], State, Final) :-
    room_step(Action, State, Next),
    check_room_plan(Rest, Next, Final).
