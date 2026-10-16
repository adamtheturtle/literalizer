-module(fixture_coercion_uniform_dict_shapes_toml_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "_" => [#{"type" => "create", "name" => "a"}, #{"type" => "update", "name" => "b"}]
    },
    My_data.
