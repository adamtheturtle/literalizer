-module(fixture_call_haxe_regex_binding_comment_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = (~/\//).match("/") ? make_widget(42) : null // trailing,
    My_data.
