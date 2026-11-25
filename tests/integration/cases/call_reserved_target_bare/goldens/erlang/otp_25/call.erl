-module(fixture_call_reserved_target_bare_erlang_call).
-export([x/0]).
class(_) -> ok.
x() ->
    class(42).
