-module(fixture_elm_wrapped_call_result_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(1),
    My_data.
