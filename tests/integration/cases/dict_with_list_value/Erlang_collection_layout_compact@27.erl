-module(fixture_dict_with_list_value_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "scores" => [10, 20, 30]
    },
    My_data.
