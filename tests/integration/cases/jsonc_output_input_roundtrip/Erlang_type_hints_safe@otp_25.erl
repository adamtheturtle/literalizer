-module(fixture_jsonc_output_input_roundtrip_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        % heading
        "count" => 2
    },
    My_data.
