-module(check).
-export([x/0]).
x() ->
    My_data = [
        2#0,
        2#1,
        -2#1
    ],
    My_data.
