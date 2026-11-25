class Fixture_literalize_ref_toml_table_Haxe_ref {
    public static function main() {
        final myVar = ([
            "_" => "_",
        ] : Map<String, Dynamic>);
        final my_data = ([
            "key" => myVar,
        ] : Map<String, Dynamic>);
    }
}
