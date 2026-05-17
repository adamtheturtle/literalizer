-module(fixture_time_union_nested_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "mixed" => [["09:30:00"], []]
    },
    My_data.
