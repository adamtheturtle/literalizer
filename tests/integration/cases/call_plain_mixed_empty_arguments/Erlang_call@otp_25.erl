-module(fixture_call_plain_mixed_empty_arguments_erlang_call).
-export([x/0]).
make_widget(_, _, _) -> undefined.
x() ->
    make_widget([], [1], []),
    make_widget(["text"], [2], []),
    make_widget([], ["text"], []),
    make_widget(["text"], [2], [3]).
