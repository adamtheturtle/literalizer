-module(fixture_scalar_time_microsecond_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"exact_millisecond"/utf8>> => <<"09:30:15.123000"/utf8>>,
        <<"sub_millisecond"/utf8>> => <<"09:30:15.123456"/utf8>>
    },
    My_data.
