-module(fixture_record_named_nested_record_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "project" => "alpha",
        "lead_task" => #{"id" => 100, "description" => "first task", "is_done" => false, "blocks" => [102, 103]}
    },
    My_data.
