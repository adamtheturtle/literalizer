-module(check).
-export([x/0]).
x() ->
    My_data = [
        16#F4240,
        -16#4D2,
        16#FF,
        -16#A
    ],
    My_data.
