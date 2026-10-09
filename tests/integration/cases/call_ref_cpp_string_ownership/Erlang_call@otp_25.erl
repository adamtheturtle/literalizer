-module(fixture_call_ref_cpp_string_ownership_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = "s",
    consume(Item).
