-module(fixture_call_variable_form_new_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42),
    My_data.
