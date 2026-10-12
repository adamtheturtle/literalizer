-module(fixture_call_binding_inner_comment_objectivec_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42) ?
    make_widget(42) // inner
    : nil // trailing,
    My_data.
