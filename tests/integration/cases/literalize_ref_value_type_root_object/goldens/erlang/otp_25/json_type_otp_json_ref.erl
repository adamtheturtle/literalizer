-module(fixture_literalize_ref_value_type_root_object_erlang_json_type_otp_json_ref).
-export([x/0]).
x() ->
    Shared = #{
        <<"field"/utf8>> => [1, 2]
    },
    My_data = Shared,
    My_data.
