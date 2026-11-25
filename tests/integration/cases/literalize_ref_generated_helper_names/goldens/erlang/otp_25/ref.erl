-module(fixture_literalize_ref_generated_helper_names_erlang_ref).
-export([x/0]).
x() ->
    Std = #{
        "a" => 1
    },
    Arena = #{
        "a" => 1
    },
    Allocator = #{
        "a" => 1
    },
    My_data = [
        Std,
        Arena,
        Allocator
    ],
    My_data.
