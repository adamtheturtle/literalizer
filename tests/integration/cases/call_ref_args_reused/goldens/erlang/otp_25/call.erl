-module(fixture_call_ref_args_reused_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    Single_var = [
        4,
        5,
        6
    ],
    Repeated_var = 1,
    process(Repeated_var, 1),
    process(Single_var, 0),
    process(Repeated_var, 8).
