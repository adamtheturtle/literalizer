-module(fixture_call_multi_args_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process(1, 42),
    process(2, 100).
