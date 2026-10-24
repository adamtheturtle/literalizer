-module(fixture_string_with_dollar_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        "price $10",
        "$HOME"
    },
    My_data.
