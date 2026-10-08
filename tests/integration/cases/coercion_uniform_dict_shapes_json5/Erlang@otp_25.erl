-module(fixture_coercion_uniform_dict_shapes_json5_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"type" => "create", "name" => "a"},
        #{"type" => "update", "name" => "b"}
    ],
    My_data.
