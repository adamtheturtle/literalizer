-module(fixture_call_nested_inline_middle_erlang_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f([["DEL", "b", "10"], ["ADD", "a", "x"]]).  % note
