-module(fixture_ocaml_nested_arrays_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1]],
        [[]]
    ],
    My_data.
