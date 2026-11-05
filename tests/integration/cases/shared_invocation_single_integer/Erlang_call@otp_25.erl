-module(fixture_shared_invocation_single_integer_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    consume(1).
