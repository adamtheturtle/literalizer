-module(fixture_inconsistent_string_dict_shapes_in_seq_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"first" => "Alice", "last" => "Smith"},
        #{"first" => "Bob", "middle" => "Quincy"}
    ],
    My_data.
