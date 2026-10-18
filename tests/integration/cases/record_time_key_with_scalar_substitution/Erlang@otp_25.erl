-module(fixture_record_time_key_with_scalar_substitution_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => #{"01:02:03" => 1},
        "other" => 2
    },
    My_data.
