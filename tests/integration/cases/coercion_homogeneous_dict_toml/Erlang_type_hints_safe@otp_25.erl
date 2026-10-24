-module(fixture_coercion_homogeneous_dict_toml_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "_" => #{"a" => 1, "b" => 2}
    },
    My_data.
