-module(fixture_call_bound_ref_unused_erlang_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f([1, 2]).
