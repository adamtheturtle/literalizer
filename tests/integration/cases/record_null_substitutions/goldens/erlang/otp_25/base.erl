-module(fixture_record_null_substitutions_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"rows", [#{"replacement" => -1, "present" => 1}, #{"replacement" => 2, "present" => 3}]}
    ],
    My_data.
