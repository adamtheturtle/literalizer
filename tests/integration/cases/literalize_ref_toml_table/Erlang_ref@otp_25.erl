-module(fixture_literalize_ref_toml_table_erlang_ref).
-export([x/0]).
x() ->
    My_var = #{
        "_" => "_"
    },
    My_data = #{
        "key" => My_var
    },
    My_data.
