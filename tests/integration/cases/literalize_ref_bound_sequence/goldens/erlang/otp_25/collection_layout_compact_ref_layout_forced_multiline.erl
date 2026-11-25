-module(fixture_literalize_ref_bound_sequence_erlang_collection_layout_compact_ref_layout_forced_multiline).
-export([x/0]).
x() ->
    Ref_data = [
        1,
        2
    ],
    My_data = Ref_data,
    My_data.
