class Fixture_string_nul_before_hex_Haxe {
    public static function main() {
        final my_data = ([
            "x" => "before\x00after",
        ] : Map<String, Dynamic>);
    }
}
