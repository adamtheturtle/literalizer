-module(fixture_call_dispatch_erlang_call).
-export([x/0]).
store_item(_, _) -> ok.
read_item(_) -> ok.
x() ->
    store_item(1, 10),
    read_item(1).
