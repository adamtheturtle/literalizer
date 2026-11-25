-module(fixture_multiline_sibling_list_widening_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "omap_value" => [{"first", 1}],
        "sibling_lists" => #{"numbers" => [1, 2], "strings" => ["x", "y"]},
        "ref_marker_present" => ["$keep", "z"]
    },
    My_data.
