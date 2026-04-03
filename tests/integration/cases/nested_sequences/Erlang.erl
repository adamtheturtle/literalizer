-module(check).
-export([x/0]).
x() ->
    My_data = [
        [[1, 2], [3, 4]],
        [[5]]
    ],
    My_data.
