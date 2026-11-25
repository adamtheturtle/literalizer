-module(fixture_homogeneous_nested_map_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "first" => #{"x" => 1, "y" => 2},
        "second" => #{"z" => 3}
    },
    My_data.
