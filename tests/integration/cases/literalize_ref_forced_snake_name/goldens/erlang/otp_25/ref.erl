-module(fixture_literalize_ref_forced_snake_name_erlang_ref).
-export([x/0]).
x() ->
    User_obj = #{
        "_" => "_"
    },
    My_data = User_obj,
    My_data.
