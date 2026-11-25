class Fixture_nested_collection_multi_space_string_Haxe {
    public static function main() {
        final my_data = ([
            (["key" => "hello   world", "value" => 1] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
