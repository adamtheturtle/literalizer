-module(fixture_deep_nesting_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "level1" => #{"level2" => #{"level3" => #{"level4" => #{"value" => "deep", "items" => ["a", "b"]}}, "sibling" => 42}, "tags" => [#{"name" => "tag1", "meta" => #{"priority" => 1, "labels" => ["x", "y"]}}]}
    },
    My_data.
