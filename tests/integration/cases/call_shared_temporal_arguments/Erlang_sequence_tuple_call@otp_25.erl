-module(fixture_call_shared_temporal_arguments_erlang_sequence_tuple_call).
-export([x/0]).
check(_, _) -> ok.
x() ->
    check("2024-01-15T10:30:00+00:00", "2024-06-01").
