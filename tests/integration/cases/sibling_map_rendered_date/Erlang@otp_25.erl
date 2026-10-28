-module(fixture_sibling_map_rendered_date_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{"k" => "2020-01-01"},
        "b" => #{"k" => "string"}
    },
    My_data.
