-module(fixture_call_unused_bound_reference_erlang_sequence_tuple_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f({1, 2}).
