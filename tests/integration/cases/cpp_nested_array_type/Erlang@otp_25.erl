-module(fixture_cpp_nested_array_type_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1]]
    ],
    My_data.
