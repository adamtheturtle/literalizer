-module(fixture_call_nim_dotted_empty_result_binding_erlang_json_type_otp_json_call).
-export([x/0]).
'thing.go'(_) -> undefined.
x() ->
    My_data = 'thing.go'([]),
    My_data.
