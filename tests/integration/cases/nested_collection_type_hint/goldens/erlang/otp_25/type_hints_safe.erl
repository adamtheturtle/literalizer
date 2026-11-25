-module(fixture_nested_collection_type_hint_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [#{"b" => 1}]
    },
    My_data.
