-module(fixture_ragged_map_sequence_values_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"a"/utf8>> => [#{<<"item"/utf8>> => [1]}],
        <<"b"/utf8>> => [#{<<"item"/utf8>> => [2, 3]}]
    },
    My_data.
