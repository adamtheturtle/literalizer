-module(fixture_call_ref_string_copy_modes_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = "s",
    consume(Item).
