-module(fixture_toml_dotted_key_comments_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % first dotted key
        % second dotted key
        "a" => #{"b" => 1, "c" => 2}
    },
    My_data.
