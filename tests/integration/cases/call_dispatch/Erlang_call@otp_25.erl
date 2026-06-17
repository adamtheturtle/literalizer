-module(fixture_call_dispatch_erlang_call).
-export([x/0]).
put(_, _) -> ok.
get(_) -> ok.
x() ->
    put(1, 10),
    get(1).
