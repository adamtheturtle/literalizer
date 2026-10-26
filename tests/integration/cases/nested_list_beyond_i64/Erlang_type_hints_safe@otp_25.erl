-module(fixture_nested_list_beyond_i64_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [1],
        [1180591620717411303424]
    ],
    My_data.
