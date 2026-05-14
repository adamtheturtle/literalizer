-module(fixture_record_two_shapes_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "metrics" => #{"count" => 100, "rate" => 50},
        "flags" => #{"retries" => 3, "timeout" => 30}
    },
    My_data.
