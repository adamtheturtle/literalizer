-module(fixture_unicode_line_separators_erlang).
-export([x/0]).
x() ->
    My_data = "a\x{85}b\x{2028}c\x{2029}d",
    My_data.
