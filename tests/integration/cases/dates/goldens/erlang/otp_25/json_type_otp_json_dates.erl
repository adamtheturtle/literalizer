-module(fixture_dates_erlang_json_type_otp_json_dates).
-export([x/0]).
x() ->
    My_data = #{
        <<"date"/utf8>> => <<"2024-01-15"/utf8>>,
        <<"datetime"/utf8>> => <<"2024-01-15T12:30:00+00:00"/utf8>>
    },
    My_data.
