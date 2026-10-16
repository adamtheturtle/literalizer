-module(fixture_jsonc_comments_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % A JSONC input case with both comment forms.
        "url" => "https://example.org/a/*b*/",  % detail
        % continued
        "count" => 2  % trailing line comment
    },
    My_data.
