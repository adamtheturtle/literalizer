-module(fixture_empty_dicts_in_sequence_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        #{},
        #{}
    ],
    My_data.
