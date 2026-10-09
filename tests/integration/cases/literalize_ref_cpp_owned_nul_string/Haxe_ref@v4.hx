class Fixture_literalize_ref_cpp_owned_nul_string_Haxe_ref {
    public static function main() {
        final shared = "a\x00b";
        final my_data = ([
            "value" => shared,
        ] : Map<String, Dynamic>);
    }
}
