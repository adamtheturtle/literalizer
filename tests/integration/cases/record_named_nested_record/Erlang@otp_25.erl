-module(fixture_record_named_nested_record_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "collection" => "alpha",
        "featured_entry" => #{"id" => 100, "label" => "first entry", "enabled" => false, "related_ids" => [102, 103]}
    },
    My_data.
