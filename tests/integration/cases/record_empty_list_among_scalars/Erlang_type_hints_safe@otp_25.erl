-module(fixture_record_empty_list_among_scalars_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [1, []]
    },
    My_data.
