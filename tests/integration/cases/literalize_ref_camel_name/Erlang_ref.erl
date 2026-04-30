-module(fixture_literalize_ref_camel_name_erlang_ref).
-export([x/0]).
x() ->
    My_var = #{
        "_" => "_"
    },
    My_data = My_var,
    My_data.
