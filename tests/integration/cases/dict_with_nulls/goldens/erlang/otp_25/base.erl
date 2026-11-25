-module(fixture_dict_with_nulls_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "score" => undefined,
        "age" => 30
    },
    My_data.
