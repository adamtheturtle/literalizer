-module(fixture_comment_tabs_and_string_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % before	line
        "value" => "left\tright"  % inline	line
        % after	line
    },
    My_data.
