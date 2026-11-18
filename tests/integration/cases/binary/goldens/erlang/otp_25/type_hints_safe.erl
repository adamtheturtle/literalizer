-module(fixture_binary_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        <<72, 101, 108, 108, 111>>
    ],
    My_data.
