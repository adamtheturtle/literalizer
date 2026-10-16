-module(fixture_json5_comment_lexemes_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % heading
        "a" => "single ' // data",
        "b" => "linecontinuation",
        "c" => "\\",  % actual comment
        "d" => "\x{2028}\x{2029}"  % final comment
    },
    My_data.
