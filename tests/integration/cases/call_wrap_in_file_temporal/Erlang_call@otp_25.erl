-module(fixture_call_wrap_in_file_temporal_erlang_call).
-export([x/0]).
check(_, _) -> ok.
x() ->
    check("2024-01-15T10:30:00+00:00", "2024-06-01").
