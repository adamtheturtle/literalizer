-module(fixture_empty_orderedmap_value_in_dict_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"a"/utf8>> => [],
        <<"b"/utf8>> => 1
    },
    My_data.
