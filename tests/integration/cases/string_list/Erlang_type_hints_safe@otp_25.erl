-module(fixture_string_list_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        "foo",
        "bar",
        "baz"
    ],
    My_data.
