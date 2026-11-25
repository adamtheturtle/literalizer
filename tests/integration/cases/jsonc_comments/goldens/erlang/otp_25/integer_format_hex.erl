-module(fixture_jsonc_comments_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        % A JSONC input case with both comment forms.
        "url" => "https://example.org/a/*b*/",  % detail
        % continued
        "count" => 16#2  % trailing line comment
    },
    My_data.
