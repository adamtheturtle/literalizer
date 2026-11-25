-module(fixture_sibling_map_rendered_datetime_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{"k" => "2020-01-01T00:00:00+00:00"},
        "b" => #{"k" => "string"}
    },
    My_data.
