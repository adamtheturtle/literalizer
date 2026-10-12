-module(fixture_call_binding_inner_comment_haxe_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = (
    make_widget(42) // inner
    ) // trailing,
    My_data.
