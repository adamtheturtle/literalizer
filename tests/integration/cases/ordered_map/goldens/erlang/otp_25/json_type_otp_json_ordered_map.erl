-module(fixture_ordered_map_erlang_json_type_otp_json_ordered_map).
-export([x/0]).
x() ->
    My_data = [
        {<<"name"/utf8>>, <<"Alice"/utf8>>},
        {<<"age"/utf8>>, 30},
        {<<"active"/utf8>>, true}
    ],
    My_data.
