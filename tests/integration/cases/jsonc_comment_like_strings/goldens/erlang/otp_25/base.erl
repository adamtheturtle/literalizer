-module(fixture_jsonc_comment_like_strings_erlang).
-export([x/0]).
x() ->
    My_data = [
        "// data",
        "/* data */",
        "escaped quote: \" // data",
        "backslash: \\"
    ],
    My_data.
