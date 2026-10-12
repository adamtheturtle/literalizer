-module(fixture_call_binding_inline_comment_dart_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42) // note,
    My_data.
