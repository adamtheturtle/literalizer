-module(fixture_literalize_ref_in_dict_erlang_ref).
-export([x/0]).
x() ->
    My_var = 1,
    My_data = #{
        "key" => My_var
    },
    My_data.
