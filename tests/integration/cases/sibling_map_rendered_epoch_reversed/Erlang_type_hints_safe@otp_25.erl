-module(fixture_sibling_map_rendered_epoch_reversed_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "b" => #{"k" => 1},
        "a" => #{"k" => "2040-01-01T00:00:00+00:00"}
    },
    My_data.
