-module(fixture_mixed_number_dict_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => 2.5,
        "c" => 3
    },
    My_data.
