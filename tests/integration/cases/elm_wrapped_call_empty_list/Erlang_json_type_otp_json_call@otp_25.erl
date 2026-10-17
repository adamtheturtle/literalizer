-module(fixture_elm_wrapped_call_empty_list_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget([]).
