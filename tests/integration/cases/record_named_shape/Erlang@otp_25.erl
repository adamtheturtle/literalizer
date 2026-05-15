-module(fixture_record_named_shape_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"id" => 100, "description" => "first task", "is_done" => false, "blocks" => [102, 103]},
        #{"id" => 101, "description" => "second task", "is_done" => true, "blocks" => [100]}
    ],
    My_data.
