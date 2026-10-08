-module(fixture_crystal_record_empty_list_among_scalars_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [1, []]
    },
    My_data.
