-module(fixture_coercion_homogeneous_dict_json_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => 2
    },
    My_data.
