-module(fixture_record_two_shapes_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "user" => #{"id" => 1, "name" => "Alice"},
        "project" => #{"title" => "report", "tags" => ["draft", "urgent"]}
    },
    My_data.
