-module(fixture_java_nested_ordered_map_type_hint_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [{"b", 1}]
    },
    My_data.
