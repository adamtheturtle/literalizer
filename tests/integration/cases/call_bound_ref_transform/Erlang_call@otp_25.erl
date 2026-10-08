-module(fixture_call_bound_ref_transform_erlang_call).
-export([x/0]).
f(_) -> undefined.
x() ->
    X = 1,
    f(X).
