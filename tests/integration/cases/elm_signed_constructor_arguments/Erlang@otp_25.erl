-module(fixture_elm_signed_constructor_arguments_erlang).
-export([x/0]).
x() ->
    My_data = [
        -42,
        0,
        42,
        -1.25,
        0.0,
        1.25
    ],
    My_data.
