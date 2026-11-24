-module(fixture_long_string_before_list_comma_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
        1
    ],
    My_data.
