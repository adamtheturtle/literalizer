-module(fixture_nested_map_list_integer_widening_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [1],
        "b" => [1099511627776]
    },
    My_data.
