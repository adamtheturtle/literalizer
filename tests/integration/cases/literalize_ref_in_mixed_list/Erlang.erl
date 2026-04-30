-module(fixture_literalize_ref_in_mixed_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"$ref" => "ref_x"},
        1,
        2
    ],
    My_data.
