class Fixture_non_identifier_mapping_key_Haxe {
    public static function main() {
        final my_data = ([
            "not-a-field" => 1,
        ] : Map<String, Dynamic>);
    }
}
