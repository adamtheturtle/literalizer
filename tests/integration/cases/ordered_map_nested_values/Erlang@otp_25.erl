-module(fixture_ordered_map_nested_values_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"name", "Alice"},
        {"scores", #{
            % score meaning
            1 => "first",
            2 => "second"  % latest score
        }}
    ],
    My_data.
