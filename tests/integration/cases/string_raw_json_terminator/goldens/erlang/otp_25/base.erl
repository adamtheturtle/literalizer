-module(fixture_string_raw_json_terminator_erlang).
-export([x/0]).
x() ->
    My_data = #{
        ")json" => "x"
    },
    My_data.
