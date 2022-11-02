block(X):-
    blocks(B),
    member(X, B).

delete(E, [E|T], T).
delete(E, [H|T1], [H|T2]):-
    delete(E, T1, T2).

% move(X, Y, Z, S1, S2) holds when S2 is obtained from S1 by moving the block X from the block Y onto the block Z.
move(X, Y, Z, S1, S2):-
	member([clear, X], S1), % find a clear block X in S1
	member([on, X, Y], S1), block(Y), % find a block on which X sits
	member([clear, Z], S1), notequal(X, Z), % find another clear block, Z
	substitute([on, X, Y], [on, X, Z], S1, INT), % remove X from Y, place it on Z
	substitute([clear, Z], [clear, Y], INT, S2). % Z is no longer clear; Y is now clear

% moveToTable(X, Y, S1, S2) holds when S2 is obtained from S1 by moving the block X from the block Y onto the table.
moveToTable(X, Y, S1, [[clear, Y]|INT]):-
	member([clear, X], S1), % find a clear block X in S1
	member([on, X, Y], S1), block(Y), % find a block on which X sits
	substitute([on, X, Y], [on, X, "table"], S1, INT). % remove X from Y, place it on table

% moveFromTable(X, Y, S1, S2) holds when S2 is obtained from S1 by moving the block X from the table onto the block Z.
moveFromTable(X, Z, S1, S2):-
	member([clear, X], S1), % find a clear block X in S1
	member([on, X, "table"], S1), % ensure X is currently on the table
	member([clear, Z], S1), notequal(X, Z), % find another clear block, Z
	substitute([on, X, "table"], [on, X, Z], S1, INT), % remove X from the table, place it on Z
    delete([clear, Z], INT, S2). % Z is no longer clear


% notequal(X11, X2) holds when X1 and X2 are not equal
notequal(X, X):- !, fail.
notequal(_, _).

notmember(_,[]).
notmember(X, [X|_]):- !, fail.
notmember(X, [_|T]):-
    notmember(X, T).

% substitute(E, E1, OLD, NEW) holds when NEW is the list OLD in which E is substituted by E1.  There are no duplicates in OLD or NEW.
substitute(X, Y, [X|T1], [Y|T1]).
substitute(X, Y, [H|T], [H|T1]):- 
    substitute(X, Y, T, T1).

path(S1, S2):- move(_, _, _, S1, S2).
path(S1, S2):- moveToTable(_, _, S1, S2).
path(S1, S2):- moveFromTable(_, _, S1, S2).

%connected: symmetric version of path
connected(S1, S2) :- path(S1, S2).
connected(S1, S2) :- path(S2, S1).



% ORIGINAL (mostly) from the assignment.
notYetVisited(State, PathSoFar):-
	permute(State, PermuteState),
	\+ member(PermuteState, PathSoFar).

permute([], []).
permute(L, [X|P]):-
   delete(X, L, L2),
   permute(L2, P).

% MODIFIED, to (hopefully) be faster.
% notYetVisited(_, []).
% notYetVisited(State, [P|PS]):-
%     \+ setequal(State, P),
%     notYetVisited(State, PS).

% setequal([], []).
% setequal([X|T], S):-
%     member(X, S),
%     delete(X, S, S1),
%     setequal(T, S1).



%dfs(State1, Path, PathSoFar): returns the Path from the start to the goal states.
% Trivial: if X is the goal return X as the path from X to X.
dfs(X, [X], _):- goal(X).
% else expand X by Y and find path from Y
dfs(X, [X|Ypath], VISITED):-
    connected(X, Y),
	notYetVisited(Y, VISITED),
	dfs(Y, Ypath, [Y|VISITED]).

blocks([a, b, c, d]).
start([ [on, a, b], [on, b, "table"], [on, c, d], [clear, c], [clear, a], [on, d, "table"]]).
goal([ [on, d, a], [on, a, c], [on, c, b], [on, b, "table"], [clear, a] ]).

% To run code:
% ?- start(S1), dfs(S1, P, [S1]).

