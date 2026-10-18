-module(fixture_ordered_map_empty_key_erlang_default_empty_dict_key).
-export([x/0]).
x() ->
    My_data = [
        {"", "unnamed"},
        {"named", "value"}
    ],
    My_data.
