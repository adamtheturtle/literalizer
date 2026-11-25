-module(fixture_call_string_result_binding_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget("text"),
    My_data.
