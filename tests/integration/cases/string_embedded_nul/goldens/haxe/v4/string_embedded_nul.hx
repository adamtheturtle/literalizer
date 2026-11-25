class Fixture_string_embedded_nul_Haxe_string_embedded_nul {
    public static function main() {
        final my_data = ([
            "x" => "\x00",
            "y" => "\x001",
        ] : Map<String, Dynamic>);
    }
}
