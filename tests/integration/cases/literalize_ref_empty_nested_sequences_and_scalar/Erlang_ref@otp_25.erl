-module(fixture_literalize_ref_empty_nested_sequences_and_scalar_erlang_ref).
-export([x/0]).
x() ->
    Seed = 1,
    My_data = [
        [],
        [[]],
        Seed
    ],
    My_data.
