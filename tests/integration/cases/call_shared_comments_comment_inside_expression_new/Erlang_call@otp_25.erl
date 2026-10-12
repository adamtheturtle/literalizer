-module(fixture_call_shared_comments_comment_inside_expression_new_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42) // inner
     + 1,
    My_data.
