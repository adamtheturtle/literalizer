-module(fixture_mixed_number_dict_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 2#1,
        "b" => 2.5,
        "c" => 2#11
    },
    My_data.
