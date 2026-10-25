-module(fixture_rectangular_map_sequence_shapes_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"a"/utf8>> => [#{<<"item"/utf8>> => [1]}],
        <<"b"/utf8>> => [#{<<"item"/utf8>> => [2]}]
    },
    My_data.
