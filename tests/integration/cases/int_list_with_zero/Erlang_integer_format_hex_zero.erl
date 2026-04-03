-module(check).
-export([x/0]).
x() ->
    My_data = [
        16#0,
        16#1,
        -16#1
    ],
    My_data.
