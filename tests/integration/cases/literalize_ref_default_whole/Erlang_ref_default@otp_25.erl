-module(fixture_literalize_ref_default_whole_erlang_ref_default).
-export([x/0]).
x() ->
    My_var = #{
        "_" => "_"
    },
    My_data = My_var,
    My_data.
