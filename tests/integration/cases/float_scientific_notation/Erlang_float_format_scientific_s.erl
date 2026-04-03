-module(check).
-export([x/0]).
x() ->
    My_data = [
        0.0,
        1.0,
        1.5e3,
        1.0e-3
    ],
    My_data.
