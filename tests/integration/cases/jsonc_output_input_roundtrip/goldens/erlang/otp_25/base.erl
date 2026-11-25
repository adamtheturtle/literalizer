-module(fixture_jsonc_output_input_roundtrip_erlang).
-export([x/0]).
x() ->
    My_data = #{
        % heading
        "count" => 2
    },
    My_data.
