-module(fixture_toml_multiline_element_comments_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = #{
        "first" => [
            1,
            2
        ],
        "second" => 3  % About the second key.
    },
    My_data.
