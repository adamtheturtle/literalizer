-module(fixture_simple_dict_erlang_type_hints_safe_dt_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "age" => 30,
        "active" => true,
        "score" => undefined
    },
    My_data.
