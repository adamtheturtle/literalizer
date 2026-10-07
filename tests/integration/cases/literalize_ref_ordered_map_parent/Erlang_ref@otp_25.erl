-module(fixture_literalize_ref_ordered_map_parent_erlang_ref).
-export([x/0]).
x() ->
    Bound = 2,
    My_data = [
        {"value", Bound}
    ],
    My_data.
