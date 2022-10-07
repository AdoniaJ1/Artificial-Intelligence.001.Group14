randomList(0, []).
randomList(N, L):-
    M is N * 5,
    randomList(N, L, M).
randomList(0, [], _).
randomList(N, [R|T], M):-
    random(0, M, R),
    N1 is N - 1,
    randomList(N1,T,M).

/*swap the first two elements if they are not in order*/
swap([X, Y|T], [Y, X | T]) :- Y =< X.
/*swap elements in the tail*/
swap([H|T], [H|T1]) :- swap(T, T1).

/* */
bubbleSort(L,SL):-
    swap(L, L1), % at least one swap is needed
    !,
    bubbleSort(L1, SL).
bubbleSort(L, L). % here, the list is already sorted

/* checks if head of list is =< 2nd element and iterates through the list 
 * checking if each element is =< the preceding element until tail is empty */
ordered([]).
ordered([_X]).
ordered([H1, H2|T]):-
    H1 =< H2,
    ordered([H2|T]).

/*Comment describing insert(E, SL, SLE) ...*/
/*Comment describing the 1st clause of insert ...*/
insert(X, [],[X]).
insert(E, [H|T], [E,H|T]):-
    ordered(T),
    =<(E, H),
    !.
/*Comment describing the 2nd clause of insert ...*/
insert(E, [H|T], [H|T1]):-
    ordered(T),
    insert(E, T, T1).

/* Comment describing insertionSort */
insertionSort([], []).
insertionSort([H|T], SORTED) :-
    insertionSort(T, T1),
    insert(H, T1, SORTED).

/*
 * Given a list and a variable, performs merge sort on the list to populate the variable with the sorted list.
 * First splits the list in half, merge sorts either list, then merges them together.*/
mergeSort([], []). % the empty list is sorted
mergeSort([X], [X]) :- !.
mergeSort(L, SL):-
    split_in_half(L, L1, L2),
    mergeSort(L1, S1),
    mergeSort(L2, S2),
    merge(S1, S2, SL).

/* Populates R with the result of integer-dividing N by N1. */
intDiv(N, N1, R):- R is div(N, N1).

split_in_half([], _, _) :- !, fail.
split_in_half([X],[],[X]).
split_in_half(L, L1, L2) :-
    length(L, N),
    intDiv(N, 2, N1),
    length(L1, N1),
    append(L1, L2, L).

/* Merges sorted lists S1 and S2 into S. */
merge([], L, L). % A list merged with the empty list is that list.
merge(L, [],L).  % A list merged with the empty list is that list.
merge([H1|T1],[H2|T2],[H1|T]):-
    H1 =< H2,
    merge(T1,[H2|T2],T).
merge([H1|T1], [H2|T2], [H2|T]):-
    H2 =< H1,
    merge([H1|T1], T2, T).

/*
 * Given a median value and a list, partitions the list into the latter two variables, which are the elements less than
 * or equal to the median value and the elements greater than the median value, respectively.
 */
split(_, [],[],[]).
split(X, [H|T], [H|SMALL], BIG):-
    H =< X,
    split(X, T, SMALL, BIG).
split(X, [H|T], SMALL, [H|BIG]):-
    X =< H,
    split(X, T, SMALL, BIG).

/*
 * Given a list and a variable, performs quick sort on the list to populate the variable with the sorted list.
 * Partitions the list on the first element, then recursively quick sorts the partitions, then appends the sorted lists
 * together.
 */
quickSort([], []).
quickSort([H|T], LS):-
    split(H, T, SMALL, BIG),
    quickSort(SMALL, S),
    quickSort(BIG, B),
    append(S, [H|B], LS).

/* Comment describing hybridSort */
hybridSort(LIST, bubbleSort, _BIGALG, THRESHOLD, SLIST):-
	length(LIST, N), N =< THRESHOLD,      
    bubbleSort(LIST, SLIST).
hybridSort(LIST, insertionSort, _BIGALG, THRESHOLD, SLIST):-
	length(LIST, N), N =< THRESHOLD,
    insertionSort(LIST, SLIST).
hybridSort(LIST, SMALL, mergeSort, THRESHOLD, SLIST):-
	length(LIST, N), N > THRESHOLD,
    split_in_half(LIST, L1, L2),
    hybridSort(L1, SMALL, mergeSort, THRESHOLD, S1),
    hybridSort(L2, SMALL, mergeSort, THRESHOLD, S2),
    merge(S1,S2, SLIST).
hybridSort([H|T], SMALL, quickSort, THRESHOLD, SLIST):-
	length([H|T], N), N > THRESHOLD,      
	split(H, T, L1, L2),
	hybridSort(L1, SMALL, quickSort, THRESHOLD, S1),
	hybridSort(L2, SMALL, quickSort, THRESHOLD, S2 ),    
    append(S1, [H|S2], SLIST).
    

:- dynamic p1/1.
assert(p1(randomList(5,))).
