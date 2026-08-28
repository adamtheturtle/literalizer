-module(fixture_call_nested_inline_only_erlang_call).
-export([x/0]).
f(_, _) -> ok.
x() ->
    f(2, "hello"),  % trailing note
    f(3, "world"),  % another note.
