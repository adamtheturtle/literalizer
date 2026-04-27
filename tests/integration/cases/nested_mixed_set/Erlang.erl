-module(fixture_nested_mixed_set_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "tags" => sets:from_list([true, 42, "apple"])
    },
    My_data.
