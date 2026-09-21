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
