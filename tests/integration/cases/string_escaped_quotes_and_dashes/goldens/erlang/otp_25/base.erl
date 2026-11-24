-module(fixture_string_escaped_quotes_and_dashes_erlang).
-export([x/0]).
x() ->
    My_data = "hello \"world\" -- not a comment",
    My_data.
