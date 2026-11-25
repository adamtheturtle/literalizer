-module(fixture_call_ref_args_converted_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    My_var = [
        1,
        2,
        3
    ],
    My_other = [
        4,
        5,
        6
    ],
    process(My_var, 42),
    process(My_other, 7).
