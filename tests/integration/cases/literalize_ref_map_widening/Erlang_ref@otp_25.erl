-module(fixture_literalize_ref_map_widening_erlang_ref).
-export([x/0]).
x() ->
    String_map = #{
        "k" => "s"
    },
    My_data = [
        String_map,
        #{"k" => 1}
    ],
    My_data.
