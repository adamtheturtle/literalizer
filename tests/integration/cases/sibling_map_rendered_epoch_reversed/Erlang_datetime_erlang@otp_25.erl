-module(fixture_sibling_map_rendered_epoch_reversed_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "b" => #{"k" => 1},
        "a" => #{"k" => {{2040, 1, 1}, {0, 0, 0}}}
    },
    My_data.
