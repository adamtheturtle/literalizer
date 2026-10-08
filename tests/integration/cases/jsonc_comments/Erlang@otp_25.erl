-module(fixture_jsonc_comments_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "url" => "https://example.org/a/*b*/",
        "count" => 2
    },
    My_data.
