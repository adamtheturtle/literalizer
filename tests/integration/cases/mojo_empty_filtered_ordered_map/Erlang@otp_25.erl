-module(fixture_mojo_empty_filtered_ordered_map_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"missing", undefined}
    ],
    My_data.
