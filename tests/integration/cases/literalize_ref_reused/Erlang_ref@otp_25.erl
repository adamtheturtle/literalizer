-module(fixture_literalize_ref_reused_erlang_ref).
-export([x/0]).
x() ->
    Shared_var = #{
        "_" => "_"
    },
    My_data = [
        Shared_var,
        Shared_var
    ],
    My_data.
