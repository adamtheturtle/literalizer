-module(fixture_literalize_ref_repeated_nested_collection_erlang_ref).
-export([x/0]).
x() ->
    Shared = [
        [1, 2],
        #{"value" => 1}
    ],
    My_data = [
        Shared,
        Shared
    ],
    My_data.
