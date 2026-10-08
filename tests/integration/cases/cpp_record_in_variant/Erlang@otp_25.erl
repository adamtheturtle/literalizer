-module(fixture_cpp_record_in_variant_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "h" => [1, "a", [2, "b"], #{"k" => [true]}]
    },
    My_data.
