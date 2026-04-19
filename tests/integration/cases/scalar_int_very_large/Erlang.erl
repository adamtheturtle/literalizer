-module(check).
-export([x/0]).
x() ->
    My_data = 9223372036854775808,
    My_data.
