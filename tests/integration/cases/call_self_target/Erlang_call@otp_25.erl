-module(fixture_call_self_target_erlang_call).
-export([x/0]).
self(_) -> ok.
x() ->
    self("hello").
