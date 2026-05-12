-module(fixture_call_ref_args_heterogeneous_list_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    My_ints = [
        1,
        2,
        3
    ],
    My_strings = [
        "a",
        "b"
    ],
    My_empty = [],
    process(My_ints, 42),
    process(My_strings, 7),
    process(My_empty, 99).
