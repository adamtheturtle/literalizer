-module(fixture_literalize_ref_pre_indented_erlang_ref).
-export([x/0]).
x() ->
        Shared = [
            1,
            2
        ],
        My_data = #{
            "a" => Shared
        },
    My_data.
