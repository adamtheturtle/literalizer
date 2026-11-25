-module(fixture_null_only_ordered_map_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"missing", undefined}
    ],
    My_data.
