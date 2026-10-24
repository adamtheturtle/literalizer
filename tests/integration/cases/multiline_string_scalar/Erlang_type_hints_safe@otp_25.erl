-module(fixture_multiline_string_scalar_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = "\nroot first line\n  indented\n\nroot last line\n",
    My_data.
