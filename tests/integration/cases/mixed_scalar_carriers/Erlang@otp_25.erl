-module(fixture_mixed_scalar_carriers_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        "a",
        2.5
    ],
    My_data.
