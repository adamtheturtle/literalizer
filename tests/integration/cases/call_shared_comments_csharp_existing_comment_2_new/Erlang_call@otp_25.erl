-module(fixture_call_shared_comments_csharp_existing_comment_2_new_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42) // note
    // extra,
    My_data.
