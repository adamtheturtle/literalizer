-module(fixture_dict_with_list_value_erlang_json_type_otp_json_existing).
-export([x/0]).
x() ->
    My_data = #{
        <<"name"/utf8>> => <<"Alice"/utf8>>,
        <<"scores"/utf8>> => [10, 20, 30]
    },
    My_data.
