-module(fixture_ordered_map_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"name", "Alice"},
        {"age", 30},
        {"active", true}
    ],
    My_data.
