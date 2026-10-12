-module(fixture_call_binding_quoted_comment_marker_java_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget("first \"quote\"\n// string body") // note
    // extra,
    My_data.
