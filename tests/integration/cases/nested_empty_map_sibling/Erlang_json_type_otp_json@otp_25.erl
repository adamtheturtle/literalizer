-module(fixture_nested_empty_map_sibling_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        #{<<"mapping"/utf8>> => #{}},
        #{}
    ],
    My_data.
