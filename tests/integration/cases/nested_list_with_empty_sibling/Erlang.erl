-module(check).
-export([x/0]).
x() ->
    My_data = [
        [1, 2],
        [],
        [3, 4]
    ],
    My_data.
