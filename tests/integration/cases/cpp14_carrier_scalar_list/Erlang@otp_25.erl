-module(fixture_cpp14_carrier_scalar_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        "a",
        2.5
    ],
    My_data.
