-module(fixture_literalize_ref_in_mixed_list_erlang_ref).
-export([x/0]).
x() ->
    Ref_x = #{
        "_" => "_"
    },
    My_data = [
        Ref_x,
        1,
        2
    ],
    My_data.
