class Fixture_cobol_collision_existing_suffix_Haxe {
    public static function main() {
        final my_data = ([
            "a-b" => 1,
            "a-b-2" => 2,
            "a b" => 3,
        ] : Map<String, Dynamic>);
    }
}
