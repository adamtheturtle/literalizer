-module(check).
-export([x/0]).
x() ->
    My_data = [
        inf,
        -inf,
        nan
    ],
    My_data.
