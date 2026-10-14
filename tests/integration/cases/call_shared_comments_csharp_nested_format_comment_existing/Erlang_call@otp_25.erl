-module(fixture_call_shared_comments_csharp_nested_format_comment_existing_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(undefined),
    My_data = ($"{$"{1://}"}").Length >= 0 ? make_widget(42) : make_widget(42) // trailing
    // extra.
