-module(fixture_literalize_ref_unreferenced_record_value_erlang_ref).
-export([x/0]).
x() ->
    My_data = #{
        "main" => #{"x" => 1, "y" => "s"}
    },
    My_data.
