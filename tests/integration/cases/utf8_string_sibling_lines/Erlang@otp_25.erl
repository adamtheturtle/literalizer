-module(fixture_utf8_string_sibling_lines_erlang).
-export([x/0]).
x() ->
    My_data = [
        "中中中中中中中中中中中中中中中中中中中中",
        "é'é'é'é'é'é'é'é'é'é'",
        "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
    ],
    My_data.
