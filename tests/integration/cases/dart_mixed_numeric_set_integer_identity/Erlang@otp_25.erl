-module(fixture_dart_mixed_numeric_set_integer_identity_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        1.5,
        9007199254740993
    ]),
    My_data.
