-module(fixture_dict_with_nulls_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "score" => undefined,
        "age" => 16#1E
    },
    My_data.
