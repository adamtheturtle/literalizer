-module(fixture_json5_comment_nested_empty_dicts_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % outer heading
        % first empty
        "a" => #{},
        % second empty
        "b" => #{}
    },
    My_data.
