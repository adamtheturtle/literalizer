-module(fixture_date_set_erlang_json_type_otp_json_date_set).
-export([x/0]).
x() ->
    My_data = [
        <<"2024-01-15"/utf8>>,
        <<"2024-06-01"/utf8>>
    ],
    My_data.
