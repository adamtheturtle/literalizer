-module(fixture_empty_orderedmap_value_in_dict_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [],
        "b" => 1
    },
    My_data.
