-module(fixture_call_scalar_result_json_binding_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42),
    My_data.
