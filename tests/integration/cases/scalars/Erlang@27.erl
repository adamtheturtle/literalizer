-module(fixture_scalars_erlang).
-export([x/0]).
x() ->
    My_data = [
        42,
        3.14,
        true,
        false,
        "hello \"world\""
    ],
    My_data.
