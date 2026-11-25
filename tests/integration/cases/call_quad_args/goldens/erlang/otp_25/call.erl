-module(fixture_call_quad_args_erlang_call).
-export([x/0]).
process(_, _, _, _) -> ok.
x() ->
    process(1, 2, 3, 4),
    process(5, 6, 7, 8).
