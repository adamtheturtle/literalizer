-module(fixture_string_unicode_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        "café",
        "中文",
        "😀"
    },
    My_data.
