-module(fixture_call_ref_cpp_bound_null_owning_hint_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = undefined,
    consume(Item).
