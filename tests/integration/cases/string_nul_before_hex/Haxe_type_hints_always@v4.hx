class Fixture_string_nul_before_hex_Haxe_type_hints_always {
    public static function main() {
        final my_data:Map<String, Dynamic> = ([
            "x" => "before\x00after",
        ] : Map<String, Dynamic>);
    }
}
