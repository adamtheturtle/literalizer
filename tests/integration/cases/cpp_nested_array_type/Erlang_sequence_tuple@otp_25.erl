-module(fixture_cpp_nested_array_type_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {{1}}
    },
    My_data.
