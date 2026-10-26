-module(fixture_call_bound_ref_transform_erlang_call).
-export([x/0]).
f(_) -> undefined.
repr(_) -> ok.
x() ->
    Ref_data = 1,
    repr(f(Ref_data)).
