-module(fixture_yaml_nested_sequence_between_comments_erlang).
-export([x/0]).
x() ->
    My_data = [
        [
            #{"item" => "existing"},
            "kept"
            % This comment trails the first pair.
        ],
        [#{"item" => "next"}, "also kept"],
        % This comment describes the last pair.
        [#{"item" => "last"}, "kept too"]
    ],
    My_data.
