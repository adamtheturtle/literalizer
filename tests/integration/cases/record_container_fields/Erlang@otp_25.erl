-module(fixture_record_container_fields_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"id" => 1, "empty_map" => #{}, "int_map" => #{1 => "a"}, "full_set" => sets:from_list(["x", "y"]), "empty_set" => sets:from_list([])},
        #{"id" => 2, "empty_map" => #{}, "int_map" => #{1 => "b"}, "full_set" => sets:from_list(["x"]), "empty_set" => sets:from_list([])}
    ],
    My_data.
