-module(fixture_literalize_ref_repeated_mixed_sequence_erlang_ref).
-export([x/0]).
x() ->
    Shared = [
        1,
        "x"
    ],
    My_data = [
        Shared,
        Shared
    ],
    My_data.
