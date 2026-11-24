class Fixture_literalize_ref_nul_string_value_Haxe_ref {
    public static function main() {
        final shared = "a\x00b";
        final my_data = ([
            "value" => shared,
        ] : Map<String, Dynamic>);
    }
}
