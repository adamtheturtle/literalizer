-module(check).
-export([x/0]).
x() ->
    My_data = 2#10000000000000000000000000000000,
    My_data.
