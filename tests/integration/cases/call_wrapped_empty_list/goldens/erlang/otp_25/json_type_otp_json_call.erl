-module(fixture_call_wrapped_empty_list_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget([]).
