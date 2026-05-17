class Fixture_nested_mixed_set_Haxe_collection_layout_compact {
    public static function main() {
        final my_data = ([
            "name" => "Alice",
            "tags" => ([true, 42, "apple"] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
