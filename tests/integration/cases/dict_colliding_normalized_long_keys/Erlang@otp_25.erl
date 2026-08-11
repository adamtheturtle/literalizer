-module(fixture_dict_colliding_normalized_long_keys_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a_b" => 1,
        "a-b" => 2,
        "averyveryverylongkeynamethatgoesonandonandon" => 3,
        "averyveryverylongkeynamethatgoesonandmore" => 4
    },
    My_data.
