-module(fixture_literalize_ref_default_json_nested_erlang_json_type_otp_json_ref_default).
-export([x/0]).
x() ->
    Shared = 42,
    My_data = #{
        <<"refs"/utf8>> => [Shared, Shared],
        <<"quoted"/utf8>> => <<"#{shared}"/utf8>>
    },
    My_data.
