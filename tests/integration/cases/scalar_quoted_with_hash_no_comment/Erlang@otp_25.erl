-module(fixture_scalar_quoted_with_hash_no_comment_erlang).
-export([x/0]).
x() ->
    My_data = "hello # world",
    My_data.
