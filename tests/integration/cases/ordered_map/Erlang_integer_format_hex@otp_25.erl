-module(fixture_ordered_map_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        {"name", "Alice"},
        {"age", 16#1E},
        {"active", true}
    ],
    My_data.
