-module(fixture_call_shared_comments_csharp_conditional_plain_new_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(42) : make_widget(42),
    My_data.
