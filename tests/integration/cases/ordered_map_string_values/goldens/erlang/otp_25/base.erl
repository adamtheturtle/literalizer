-module(fixture_ordered_map_string_values_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"first", "one"},
        {"second", "two"},
        {"third", "three"}
    ],
    My_data.
