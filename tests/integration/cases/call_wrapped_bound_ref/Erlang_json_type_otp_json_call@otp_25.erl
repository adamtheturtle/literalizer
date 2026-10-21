-module(fixture_call_wrapped_bound_ref_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    Value = 1,
    make_widget(Value).
