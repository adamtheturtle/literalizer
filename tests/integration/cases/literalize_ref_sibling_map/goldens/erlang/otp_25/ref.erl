-module(fixture_literalize_ref_sibling_map_erlang_ref).
-export([x/0]).
x() ->
    Sibling_map = #{
        "k" => 2
    },
    My_data = [
        #{"k" => 1},
        Sibling_map
    ],
    My_data.
