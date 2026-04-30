-module(fixture_call_wrap_in_file_escaped_quote_erlang).
-export([x/0]).
x() ->
    My_data = [
        ["a\"b"]
    ],
    My_data.
