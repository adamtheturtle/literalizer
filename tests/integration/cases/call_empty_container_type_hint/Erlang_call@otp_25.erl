-module(fixture_call_empty_container_type_hint_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process([1, #{}], 42).
