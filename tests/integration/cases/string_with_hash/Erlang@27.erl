-module(fixture_string_with_hash_erlang).
-export([x/0]).
x() ->
    My_data = [
        "issue #{42}",
        "color #red"
    ],
    My_data.
