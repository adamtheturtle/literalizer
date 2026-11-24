-module(fixture_sibling_map_rendered_time_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{"k" => "07:30:00"},
        "b" => #{"k" => "string"}
    },
    My_data.
