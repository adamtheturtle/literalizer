-module(fixture_dict_string_with_del_before_hex_letter_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => "deld"
    },
    My_data.
