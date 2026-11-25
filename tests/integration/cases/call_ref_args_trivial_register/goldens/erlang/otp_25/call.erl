-module(fixture_call_ref_args_trivial_register_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    My_int = 1,
    My_bool = true,
    My_float = 3.14,
    My_list = [
        1,
        2,
        3
    ],
    process(My_int, 42),
    process(My_bool, 7),
    process(My_float, 9),
    process(My_list, 1).
