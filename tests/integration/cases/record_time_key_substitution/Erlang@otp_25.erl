-module(fixture_record_time_key_substitution_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => #{"01:02:03" => 1}
    },
    My_data.
