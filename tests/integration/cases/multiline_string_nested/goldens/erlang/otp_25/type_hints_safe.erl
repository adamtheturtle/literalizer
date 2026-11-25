-module(fixture_multiline_string_nested_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "outer" => [["nested first line\n  indented\n\nnested last line\n"]]
    },
    My_data.
