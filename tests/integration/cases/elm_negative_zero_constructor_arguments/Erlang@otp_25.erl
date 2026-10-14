-module(fixture_elm_negative_zero_constructor_arguments_erlang).
-export([x/0]).
x() ->
    My_data = [
        -0.0,
        0.0
    ],
    My_data.
