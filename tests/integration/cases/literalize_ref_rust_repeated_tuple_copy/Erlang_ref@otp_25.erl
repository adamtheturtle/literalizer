-module(fixture_literalize_ref_rust_repeated_tuple_copy_erlang_ref).
-export([x/0]).
x() ->
    Shared = {
        1,
        "x"
    },
    My_data = {
        Shared,
        Shared
    },
    My_data.
