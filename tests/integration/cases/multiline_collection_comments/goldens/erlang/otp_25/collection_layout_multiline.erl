-module(fixture_multiline_collection_comments_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [
            1,
            2,
            3
        ],  % inline a
        "b" => 2  % inline b
    },
    My_data.
