-module(fixture_empty_sequence_and_integer_set_fields_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [],
        "b" => sets:from_list([1, 2])
    },
    My_data.
