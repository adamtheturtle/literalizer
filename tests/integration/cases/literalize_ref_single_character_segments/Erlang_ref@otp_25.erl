-module(fixture_literalize_ref_single_character_segments_erlang_ref).
-export([x/0]).
x() ->
    A_b_c = #{
        "_" => "_"
    },
    My_data = A_b_c,
    My_data.
