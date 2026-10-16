-module(fixture_call_nim_plain_empty_result_binding_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget([]),
    My_data.
