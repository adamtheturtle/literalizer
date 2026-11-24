class Fixture_toml_multiline_element_comments_Haxe_collection_layout_compact {
    public static function main() {
        final my_data = ([
            "first" => ([1, 2] : Array<Dynamic>),
            "second" => 3,  // About the second key.
        ] : Map<String, Dynamic>);
    }
}
