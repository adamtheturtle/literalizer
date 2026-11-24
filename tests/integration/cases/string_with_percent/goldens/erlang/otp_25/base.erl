-module(fixture_string_with_percent_erlang).
-export([x/0]).
x() ->
    My_data = [
        "100% done",
        "%(name) is here"
    ],
    My_data.
