-module(fixture_call_bound_ref_transform_erlang_call).
-export([x/0]).
f(_) -> undefined.
x() ->
    Ref_data = 1,
    f(Ref_data).
