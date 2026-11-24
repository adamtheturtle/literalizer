-module(fixture_multiline_string_nested_list_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        ["\nfirst line\n  indented\n\nlast line\n"]
    ],
    My_data.
