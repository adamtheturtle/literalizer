class Fixture_literalize_ref_string_value_Haxe_ref {
    public static function main() {
        final shared = "s";
        final my_data = ([
            "value" => shared,
        ] : Map<String, Dynamic>);
    }
}
