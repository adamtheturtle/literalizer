-module(fixture_int_key_dict_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        16#1 => "one",
        16#2 => "two",
        16#2A => "answer"
    },
    My_data.
