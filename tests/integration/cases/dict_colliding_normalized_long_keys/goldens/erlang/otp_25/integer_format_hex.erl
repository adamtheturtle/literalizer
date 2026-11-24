-module(fixture_dict_colliding_normalized_long_keys_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "a_b" => 16#1,
        "a-b" => 16#2,
        "averyveryverylongkeynamethatgoesonandonandon" => 16#3,
        "averyveryverylongkeynamethatgoesonandmore" => 16#4
    },
    My_data.
