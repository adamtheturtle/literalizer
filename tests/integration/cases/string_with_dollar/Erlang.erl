-module(fixture_string_with_dollar_erlang).
-export([x/0]).
x() ->
    My_data = [
        "price $10",
        "$HOME"
    ],
    My_data.
