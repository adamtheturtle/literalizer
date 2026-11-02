-module(fixture_jsonc_output_timestamp_input_roundtrip_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % event time
        "when" => "2024-01-15T12:34:56+00:00"
    },
    My_data.
