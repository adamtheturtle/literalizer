-module(fixture_map_of_dict_lists_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [#{"k" => 1}],
        "b" => [#{"k" => 2}]
    },
    My_data.
