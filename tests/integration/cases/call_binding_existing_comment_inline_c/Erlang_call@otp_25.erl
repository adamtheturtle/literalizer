-module(fixture_call_binding_existing_comment_inline_c_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42),
    My_data = make_widget(My_data) // note,
    make_widget(My_data).
