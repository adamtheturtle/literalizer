-module(fixture_mojo_scalar_variant_list_empty_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        [1, "value"],
        []
    ],
    My_data.
