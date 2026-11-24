-module(fixture_json5_comment_strings_erlang).
-export([x/0]).
x() ->
    My_data = [
        % strings stay data
        "https://example.org/a/*b*/",  % URL annotation
        "escaped quote: \" // still data",
        "backslash: \\",  % outside the string
        "/* not a comment */"
    ],
    My_data.
