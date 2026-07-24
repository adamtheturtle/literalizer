-module(fixture_record_named_nested_record_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "project" => "alpha",
        "lead_item" => #{"id" => 100, "label" => "first item", "enabled" => false, "related_ids" => [102, 103]}
    },
    My_data.
