-module(fixture_call_variable_form_no_args_erlang_call).
-export([x/0]).
make_widget() -> undefined.
x() ->
    My_data = make_widget(),
    My_data.
