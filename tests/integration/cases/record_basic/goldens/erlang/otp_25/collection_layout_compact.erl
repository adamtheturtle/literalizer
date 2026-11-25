-module(fixture_record_basic_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "id" => 1,
        "label" => "She said \"hello\", then waved",
        "enabled" => false,
        "related_ids" => [1, 2, 3]
    },
    My_data.
