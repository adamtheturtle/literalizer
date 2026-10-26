-module(fixture_nested_empty_list_map_sibling_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        #{<<"values"/utf8>> => []},
        #{}
    ],
    My_data.
