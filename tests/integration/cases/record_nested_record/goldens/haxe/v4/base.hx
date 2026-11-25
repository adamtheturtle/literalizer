class Fixture_record_nested_record_Haxe {
    public static function main() {
        final my_data = ([
            "id" => 1,
            "owner" => (["name" => "Alice", "age" => 30] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
