-module(fixture_ordered_map_int_keys_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"1", "one"},
        {"2", "two"},
        {"42", "answer"}
    ],
    My_data.
