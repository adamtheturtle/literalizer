-module(fixture_ordered_integer_map_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"a", 1},
        {"b", 2}
    ],
    My_data.
