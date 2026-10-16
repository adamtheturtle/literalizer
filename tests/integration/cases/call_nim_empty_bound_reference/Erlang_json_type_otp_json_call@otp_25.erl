-module(fixture_call_nim_empty_bound_reference_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    Items = [],
    make_widget(Items).
