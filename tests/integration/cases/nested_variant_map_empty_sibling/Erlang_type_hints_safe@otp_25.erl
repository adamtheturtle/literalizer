-module(fixture_nested_variant_map_empty_sibling_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        #{"nested" => #{"count" => 1, "name" => "value"}},
        #{}
    ],
    My_data.
