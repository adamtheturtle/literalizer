-module(fixture_call_four_args_erlang_call).
-export([x/0]).
process(_, _, _, _) -> ok.
x() ->
    process(1, 2, 3, 4),
    process(10, 20, 30, 40).
