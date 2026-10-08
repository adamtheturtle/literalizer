-module(fixture_java_call_binding_trailing_comment_erlang_type_hints_safe_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42)
    // note,
    My_data.
