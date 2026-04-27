-module(fixture_comments_nested_mapping_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{"x" => 1},
        "b" => 2
    },
    My_data.
