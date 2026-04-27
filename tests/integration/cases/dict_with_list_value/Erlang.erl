-module(fixture_dict_with_list_value_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "scores" => [10, 20, 30]
    },
    My_data.
