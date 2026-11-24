-module(fixture_int_key_dict_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        2#1 => "one",
        2#10 => "two",
        2#101010 => "answer"
    },
    My_data.
