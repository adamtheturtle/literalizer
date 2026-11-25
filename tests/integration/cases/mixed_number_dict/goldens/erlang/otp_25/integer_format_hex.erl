-module(fixture_mixed_number_dict_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 16#1,
        "b" => 2.5,
        "c" => 16#3
    },
    My_data.
