-module(fixture_orderedmap_with_annotated_value_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"a", []},
        {"b", 1}
    ],
    My_data.
