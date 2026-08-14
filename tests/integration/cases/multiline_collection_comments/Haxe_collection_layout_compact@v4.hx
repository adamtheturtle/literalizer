class Fixture_multiline_collection_comments_Haxe_collection_layout_compact {
    public static function main() {
        final my_data = ([
            "a" => ([1, 2, 3] : Array<Dynamic>),  // inline a
            "b" => 2,  // inline b
        ] : Map<String, Dynamic>);
    }
}
