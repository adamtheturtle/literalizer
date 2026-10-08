-module(fixture_jsonc_escaped_quote_slashes_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "text" => "a\"//b"
    },
    My_data.
