-module(fixture_heterogeneous_list_with_string_erlang).
-export([x/0]).
x() ->
    My_data = [
        "hello",
        42
    ],
    My_data.
