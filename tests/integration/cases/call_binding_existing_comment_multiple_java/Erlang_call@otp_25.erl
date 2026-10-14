-module(fixture_call_binding_existing_comment_multiple_java_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(undefined),
    My_data = make_widget(42) // note
    // extra.
