-module(fixture_deep_list_cousin_empty_map_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"items" => [#{"inner" => #{"x" => 1}}, #{"inner" => #{}}]},
        #{"items" => [#{"inner" => #{"x" => 2}}, #{"inner" => #{}}]}
    ],
    My_data.
