-module(fixture_dict_colliding_normalized_long_keys_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        "a_b" => 2#1,
        "a-b" => 2#10,
        "averyveryverylongkeynamethatgoesonandonandon" => 2#11,
        "averyveryverylongkeynamethatgoesonandmore" => 2#100
    },
    My_data.
