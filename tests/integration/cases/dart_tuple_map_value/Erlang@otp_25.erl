-module(fixture_dart_tuple_map_value_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "rows" => [#{"x" => 1, "y" => "a"}, #{"x" => 2, "y" => "b"}]
    },
    My_data.
