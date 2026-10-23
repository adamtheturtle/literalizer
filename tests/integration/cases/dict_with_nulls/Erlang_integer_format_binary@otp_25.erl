-module(fixture_dict_with_nulls_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "score" => undefined,
        "age" => 2#11110
    },
    My_data.
