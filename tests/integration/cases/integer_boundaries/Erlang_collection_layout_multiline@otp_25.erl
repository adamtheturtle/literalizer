-module(fixture_integer_boundaries_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = [
        -9223372036854775808,
        9223372036854775808
    ],
    My_data.
