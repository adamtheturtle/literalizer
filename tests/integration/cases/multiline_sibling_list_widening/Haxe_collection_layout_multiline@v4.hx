class Fixture_multiline_sibling_list_widening_Haxe_collection_layout_multiline {
    public static function main() {
        final my_data = ([
            "omap_value" => ([
                "first" => 1,
            ] : Map<String, Dynamic>),
            "sibling_lists" => ([
                "numbers" => ([
                    1,
                    2,
                ] : Array<Dynamic>),
                "strings" => ([
                    "x",
                    "y",
                ] : Array<Dynamic>),
            ] : Map<String, Dynamic>),
            "ref_marker_present" => ([
                "$keep",
                "z",
            ] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
