-module(fixture_mixed_type_dicts_in_sequence_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        #{"type" => "create", "pr_id" => "pr_1", "draft" => true},
        #{"type" => "create", "pr_id" => "pr_2"}
    ],
    My_data.
