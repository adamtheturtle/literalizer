-module(fixture_toml_nested_comments_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % About the first dotted key.
        % About the second dotted key.
        "dotted" => #{"first" => 1, "second" => 2},
        "plain" => 3,  % About the plain key.
        % Before the first entry.
        % Before the second entry.
        "entries" => [#{"name" => "one"}, #{"name" => "two"}],
        % Inside the table.
        "table" => #{"inner" => 4}
    },
    My_data.
