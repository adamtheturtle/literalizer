-module(fixture_literalize_ref_cpp_repeated_owned_erlang_ref).
-export([x/0]).
x() ->
    Shared = [
        1,
        2
    ],
    My_data = [
        Shared,
        Shared
    ],
    My_data.
