-module(fixture_root_reference_marker_is_data_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "$ref" => "schema.json"
    },
    My_data.
