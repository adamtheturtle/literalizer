-module(fixture_call_reserved_target_erlang_call).
-export([x/0]).
op(_) -> ok.
x() ->
    op("hello").
