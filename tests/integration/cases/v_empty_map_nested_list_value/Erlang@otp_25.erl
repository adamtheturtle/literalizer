-module(fixture_v_empty_map_nested_list_value_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"values" => [[]]}, #{}],
        [#{}, #{"values" => [[]]}]
    ],
    My_data.
