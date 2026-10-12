-module(fixture_call_shared_comments_haxe_existing_regex_comment_new_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = (~/\//).match("/") ? make_widget(42) : null // trailing,
    My_data.
