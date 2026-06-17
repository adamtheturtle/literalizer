-module(fixture_call_dispatch_transform_erlang_call).
-export([x/0]).
record(_) -> undefined.
flush(_) -> ok.
x() ->
    record(42),
    flush(3).
