-module(fixture_dict_with_homogeneous_annotated_values_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [],
        "b" => []
    },
    My_data.
