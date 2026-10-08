-module(fixture_literalize_ref_cpp_mixed_sibling_maps_erlang_ref).
-export([x/0]).
x() ->
    Actual = 42,
    My_data = [
        #{"$ref" => 1},
        #{"$ref" => undefined},
        Actual
    ],
    My_data.
