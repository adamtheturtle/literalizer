class Fixture_ordered_map_nested_record_fields_Haxe {
    public static function main() {
        final my_data = ([
            "first" => (["x" => 1] : Map<String, Dynamic>),
            "second" => (["y" => 2] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
