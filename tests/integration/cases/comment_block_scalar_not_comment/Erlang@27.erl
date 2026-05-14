-module(fixture_comment_block_scalar_not_comment_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "description" => "# not a comment\n",
        "name" => "foo"
    },
    My_data.
