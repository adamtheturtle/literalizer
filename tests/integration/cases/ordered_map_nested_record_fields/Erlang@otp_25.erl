-module(fixture_ordered_map_nested_record_fields_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"first", #{"x" => 1}},
        {"second", #{"y" => 2}}
    ],
    My_data.
