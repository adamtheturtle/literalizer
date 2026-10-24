-module(fixture_ordered_map_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        {"name", "Alice"},
        {"age", 2#11110},
        {"active", true}
    ],
    My_data.
