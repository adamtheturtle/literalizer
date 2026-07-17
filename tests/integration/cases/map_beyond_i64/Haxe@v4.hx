class Fixture_map_beyond_i64_Haxe {
    public static function main() {
        final my_data = ([
            "a" => 9223372036854775807,
            "b" => 9223372036854775808,
        ] : Map<String, Dynamic>);
    }
}
