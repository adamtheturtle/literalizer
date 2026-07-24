-module(fixture_record_named_shape_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"id" => 100, "label" => "first entry", "enabled" => false, "related_ids" => [102, 103]},
        #{"id" => 101, "label" => "second entry", "enabled" => true, "related_ids" => [100]}
    ],
    My_data.
