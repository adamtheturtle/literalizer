-module(fixture_nested_list_beyond_i64_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        [16#1],
        [16#400000000000000000]
    ],
    My_data.
