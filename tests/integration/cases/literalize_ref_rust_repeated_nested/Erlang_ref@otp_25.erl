-module(fixture_literalize_ref_rust_repeated_nested_erlang_ref).
-export([x/0]).
x() ->
    Shared = [
        1,
        2
    ],
    My_data = [
        #{"left" => Shared, "right" => Shared}
    ],
    My_data.
