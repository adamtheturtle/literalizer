-module(fixture_literalize_ref_heterogeneous_list_erlang_ref).
-export([x/0]).
x() ->
    One = 1,
    Two = "s",
    My_data = [
        One,
        Two
    ],
    My_data.
