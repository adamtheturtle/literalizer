-module(fixture_dict_mixed_scalars_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => "x"
    },
    My_data.
